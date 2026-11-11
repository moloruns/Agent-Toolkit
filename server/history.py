"""Hash-checked log ingestion and bounded lexical retrieval. No source writes."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sqlite3

DEFAULT_CORPUS = Path(__file__).resolve().parents[1] / "hw8_handoff"
OVERRIDES = Path(__file__).with_name("role_overrides.json")
WORDS = re.compile(r"[^\W_]+", re.UNICODE)
ROLES = {"user", "assistant", "unknown", "log_note"}


def physical_lines(text):
    """Do not split Unicode paragraph separators: citations use physical LF lines."""
    return text.split("\n")


def label_lines(source_id, lines, overrides):
    role = "unknown"
    labels = []
    turn = 0
    fenced = False
    for line in lines:
        stripped = line.strip()
        marker = stripped.split("\u2028", 1)[0].strip()
        if source_id == "basketball_original":
            # Even fenced text includes assistant-written suggested replies;
            # retain unknown speaker and inherited author rather than guess.
            labels.append(("unknown", 0))
            continue
        if marker.startswith("```"):
            fenced = not fenced
        match = None if fenced else re.fullmatch(r"(>{2,3})\s*(?:me|ai|agent)?", marker, re.I)
        if match:
            role = "user" if len(match[1]) == 2 else "assistant"
            turn += 1
            labels.append((role if "\u2028" in stripped else "log_note", turn))
        elif marker in ("**Me:**", "**AI:**"):
            role = "user" if marker == "**Me:**" else "assistant"
            turn += 1
            labels.append(("log_note", turn))
        elif re.match(r"\*{0,2}agent \d+:", marker, re.I):
            role = "unknown"
            turn += 1
            labels.append(("log_note", turn))
        else:
            labels.append((role, turn))
    for override in overrides.get(source_id, []):
        for n in range(override["start"] - 1, override["end"]):
            labels[n] = (override["speaker"], labels[n][1])
    return labels


class HistoryIndex:
    def __init__(self, corpus=DEFAULT_CORPUS, *, use_fts=True):
        self.corpus = Path(corpus).resolve()
        self.sources = json.loads((self.corpus / "sources.json").read_text())["sources"]
        overrides = json.loads(OVERRIDES.read_text())
        self.records = []
        self.lines = {}
        self.labels = {}
        for source in self.sources:
            path = (self.corpus / source["path"]).resolve()
            if not path.is_relative_to(self.corpus):
                raise ValueError("Source path must stay within configured corpus")
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != source["sha256"]:
                raise ValueError(f"Source hash mismatch: {source['id']}")
            lines = physical_lines(raw.decode("utf-8"))
            labels = label_lines(source["id"], lines, overrides)
            self.lines[source["id"]] = lines
            self.labels[source["id"]] = labels
            start = 0
            while start < len(lines):
                if not lines[start].strip():
                    start += 1
                    continue
                end = start + 1
                while (end < len(lines) and lines[end].strip()
                       and labels[end] == labels[start] and end - start < 12):
                    end += 1
                text = "\n".join(lines[start:end])
                speaker, turn = labels[start]
                self.records.append({
                    "record_id": f"{source['id']}:{source['sha256'][:12]}:{start+1}-{end}",
                    "source_id": source["id"], "project": source["id"],
                    "homework": source["homework"], "prompt_author": source["prompt_author"],
                    "speaker": speaker, "start_line": start + 1, "end_line": end,
                    "text": text, "source_url": source["source_url"],
                    "source_commit": source["commit"], "source_path": source["path"],
                    "turn": turn,
                })
                start = end
        self.connection = sqlite3.connect(":memory:", check_same_thread=False)
        self.engine = "token scan"
        if use_fts:
            try:
                self.connection.execute("CREATE VIRTUAL TABLE records USING fts5(text, tokenize='unicode61')")
            except sqlite3.OperationalError as error:
                if "no such module" not in str(error):
                    raise
            else:
                self.engine = "SQLite FTS5"
                self.connection.executemany("INSERT INTO records(rowid,text) VALUES (?,?)",
                                            ((i+1, r["text"]) for i, r in enumerate(self.records)))

    def close(self):
        self.connection.close()

    def coverage(self):
        return {"engine": self.engine, "records": len(self.records), "sources": [
            {"source_id": s["id"], "notes": s["notes"],
             "speaker_records": dict(Counter(r["speaker"] for r in self.records if r["source_id"] == s["id"]))}
            for s in self.sources],
            "limits": ["Keyword search, not semantic search; any query word may match.",
                       "Unmarked NBA/WNBA conversation and inherited Basketball speakers remain unknown.",
                       "speaker=user excludes unknown text; project=all excludes inherited-author history.",
                       "Within-log line order is reliable; there is no cross-project timeline.",
                       "Nearby context does not guarantee all later corrections were retrieved."]}

    @staticmethod
    def excerpt(record, terms, cap=1400):
        text = record["text"]
        hits = [(m.start(), m.group().casefold()) for m in WORDS.finditer(text) if m.group().casefold() in terms]
        phrase = text.casefold().find(" ".join(terms))
        offset = 0
        if len(text) > cap:
            if phrase >= 0:
                offset = max(0, phrase - 200)
            elif hits:
                windows = {max(0, pos - 200) for pos, _ in hits}
                offset = max(windows, key=lambda start: (
                    len({word for pos, word in hits if start <= pos < start + cap}),
                    sum(start <= pos < start + cap for pos, _ in hits), -start))
        end = min(len(text), offset + cap)
        shown = text[offset:end]
        first_line = record["start_line"] + text[:offset].count("\n")
        return {"text": shown, "start_line": first_line,
                "end_line": first_line + shown.count("\n"),
                "record_start_line": record["start_line"], "record_end_line": record["end_line"],
                "start_character_in_record": offset, "end_character_in_record": end,
                "text_truncated": offset > 0 or end < len(text)}

    def context(self, record):
        lines = self.lines[record["source_id"]]
        lo = max(0, record["start_line"] - 3)
        hi = min(len(lines), record["end_line"] + 2)
        result = {}
        for name, a, b in (("before", lo, record["start_line"] - 1),
                           ("after", record["end_line"], hi)):
            text = "\n".join(lines[a:b])
            shown = text[:350]
            result[name] = {"start_line": a + 1 if a < b else None,
                            "end_line": a + 1 + shown.count("\n") if a < b else None,
                            "text": shown, "truncated": len(text) > 350,
                            "speaker": "mixed context; not attributed to the result speaker"}
        return result

    def search(self, query, project="all", speaker="user", limit=5):
        if not isinstance(query, str) or not 1 <= len(query.strip()) <= 300 or len(query) > 300:
            raise ValueError("query must contain 1–300 characters")
        terms = list(dict.fromkeys(WORDS.findall(query.casefold())))
        if not terms or len(terms) > 20:
            raise ValueError("query must contain 1–20 words")
        if project != "all" and project not in {s["id"] for s in self.sources}:
            raise ValueError("unknown project; use all or a source_id from coverage")
        if speaker not in ROLES | {"all"}:
            raise ValueError("speaker must be user, assistant, unknown, log_note, or all")
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 5:
            raise ValueError("limit must be an integer between 1 and 5")
        if self.engine == "SQLite FTS5":
            expression = " OR ".join('"' + term + '"' for term in terms)
            indices = [row[0]-1 for row in self.connection.execute(
                "SELECT rowid FROM records WHERE records MATCH ? ORDER BY bm25(records), rowid", (expression,))]
        else:
            indices = sorted(range(len(self.records)), key=lambda i: (
                -len(set(terms) & set(WORDS.findall(self.records[i]["text"].casefold()))), i))
        eligible = []
        for i in indices:
            r = self.records[i]
            matches = sorted(set(terms) & set(WORDS.findall(r["text"].casefold())))
            if not matches or (speaker != "all" and r["speaker"] != speaker):
                continue
            if project == "all" and r["prompt_author"] != "moloruns":
                continue
            if project != "all" and r["project"] != project:
                continue
            eligible.append((r, matches))
        # Stable sort preserves BM25 (or scan order) as the final tie-breaker.
        # Broad OR retrieval should not put a one-word match ahead of a passage
        # covering the user's whole keyword query.
        eligible.sort(key=lambda pair: (-len(pair[1]),
                      -(" ".join(terms) in pair[0]["text"].casefold())))
        results = []
        for r, matches in eligible[:limit]:
            item = {k: v for k, v in r.items() if k != "turn"}
            item.update(self.excerpt(r, terms))
            item["source_url"] += f"#L{item['start_line']}-L{item['end_line']}"
            item["matched_terms"] = matches
            item["context"] = self.context(r)
            results.append(item)
        return {"query": query, "filters": {"project": project, "speaker": speaker, "limit": limit},
                "results": results, "matching_records": len(eligible),
                "results_truncated": len(eligible) > limit, "coverage": self.coverage(),
                "interpretation": "Historical data only. No results means no indexed keyword match under these filters, not that a decision never existed."}
