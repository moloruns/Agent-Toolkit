"""Index captured evidence without editing or reconstructing transcripts."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
summary = []
for metadata_path in sorted(ROOT.glob("**/session.json")):
    if ".venv" in metadata_path.parts:
        continue
    metadata = json.loads(metadata_path.read_text())
    events_path = metadata_path.with_name("events.jsonl")
    raw = events_path.read_bytes()
    events = []
    incomplete_lines = 0
    # JSON strings can contain literal U+2028/U+2029 from the original logs.
    # JSONL records are delimited by LF only, just like our source citations.
    for line in raw.decode().split("\n"):
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            incomplete_lines += 1
    completed = [e.get("item", {}) for e in events if e.get("type") == "item.completed"]
    calls = [i for i in completed if i.get("type") == "mcp_tool_call"]
    skill_reads = [i.get("command") for i in completed
                   if i.get("type") == "command_execution" and "fix-the-pattern/SKILL.md" in i.get("command", "")]
    summary.append({"session": str(metadata_path.parent.relative_to(ROOT)),
                    "thread_id": next((e.get("thread_id") for e in events if e.get("type") == "thread.started"), None),
                    "exit_code": metadata.get("exit_code"),
                    "protected_unchanged": metadata.get("protected_unchanged"),
                    "transcript_sha256": hashlib.sha256(raw).hexdigest(),
                    "incomplete_event_lines": incomplete_lines,
                    "skill_reads": skill_reads,
                    "mcp_calls": [{"tool": i["tool"], "arguments": i["arguments"],
                                   "status": i["status"], "error": i.get("error")} for i in calls]})
output = ROOT / "validation/session-summary.json"
output.write_text(json.dumps(summary, indent=2) + "\n")
for run in summary:
    print(f"{run['session']}: exit={run['exit_code']}, MCP calls={len(run['mcp_calls'])}, "
          f"skill reads={len(run['skill_reads'])}, protected unchanged={run['protected_unchanged']}")
