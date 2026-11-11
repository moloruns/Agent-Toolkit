# Build record — AI-generated working notes

This is an implementation/evidence index, not any of the three human-authored
submission documents. No live Game Finder or PokeJam application was run.

## Implementation facts

- `skills/fix-the-pattern/SKILL.md`: report-only checker. The user's refinement
  during this session was **"Emphasize understanding my intent"**. The checker
  distinguishes explicit requirements from interpretation and marks unresolved
  intent UNKNOWN before judging the other criteria.
- `server/history_server.py`: one MCP stdio tool, `search_prompt_history`.
- `server/history.py`: verifies all seven source hashes and rebuilds a small
  in-memory index at startup. SQLite FTS5 is preferred; token scan is the
  fallback. No embedding API, API key, persistent database, or network request
  is used by the server.
- `server/role_overrides.json`: reviewed attribution corrections, separate from
  unchanged logs. Most unmarked HW3 text and the inherited author's mixed-origin
  HW7 log remain `unknown`; these are searchable with `speaker="all"`.
- Keywords match literally, with OR retrieval. Ranking prefers the number of
  query words covered, then a consecutive phrase, then FTS relevance. This is
  a lexical lookup, not a semantic-search claim.
- Excerpts contain exact raw text and physical LF line locations. Long excerpts
  include character offsets and truncation flags. Context is separately labeled
  and bounded; later corrections still require follow-up searches.

## Reproduction commands

Tested environment: macOS arm64, Python 3.13.7, SQLite 3.50.4 with FTS5,
MCP SDK 2.3.0, Codex CLI 0.162.0-alpha.17.2. Fresh sessions inherit the user's
configured model. No other client has been tested.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python server/build_index.py
.venv/bin/python -m unittest discover -s tests -v
```

For Codex repository skill discovery, copy the `fix-the-pattern` folder into
`.agents/skills/` in the target repository. This checkout instead links
`.agents/skills/fix-the-pattern` to the canonical `skills/fix-the-pattern` folder.
For user-wide discovery, the official docs identify `~/.agents/skills/`.

`config/codex.example.toml` contains the registration table with a conspicuous
absolute-path placeholder. Substitute the checkout path and add the table to
the client's configuration without replacing unrelated settings. This machine
also has an ignored project `.codex/config.toml` with actual paths. A new session
must discover the skill and server; the current chat's tool catalog is not proof.

The recorded test sessions explicitly supply the same MCP registration through
CLI `-c` arguments. They use Codex's automatic approval review. A first
noninteractive attempt failed because its approval policy was `never`;
registration itself succeeded. The successful retry is preserved separately.

## Evidence navigation

| Artifact | What it establishes |
| --- | --- |
| `validation/discovery/` | Temporary skill, input prompt, actual skill file read, and unique response marker. |
| `validation/mcp-probe/transport.json` | Direct SDK transport response; this alone is not agent integration evidence. |
| `validation/mcp-probe/events.jsonl` | Initial agent tool call rejected by noninteractive approval policy. |
| `validation/mcp-probe/approved/events.jsonl` | Successful genuine agent MCP call returning the real Game Finder excerpt. |
| `validation/checks/tests.txt` | Latest ingestion, attribution, retrieval, validation, fallback, integrity, and stdio test results. |
| `validation/checks/skill-validation.txt` | Bundled skill-creator validator result; syntax only, not behavior. |
| `validation/retrieval-iteration/` | Actual wrong top result, failing regression, and corrected result for the same query. |
| `versions/history-v1/` | Retrieval/server source before the ranking and excerpt correction. |
| `versions/fix-the-pattern-v1/SKILL.md` | Checker preserved before first behavioral review. |
| `versions/fix-the-pattern-v2/SKILL.md` | Adds precise comparison with existing cases before requesting missing coverage. |
| `versions/fix-the-pattern-v3/SKILL.md` | Final checker, with criterion-specific status anchors. |
| `demos/run-a/producer/` | Fresh Game Finder producer's prompt, unedited events, response, and integrity metadata. |
| `demos/run-b/producer/` | Fresh PokeJam producer's prompt, unedited events, response, and integrity metadata. |
| `demos/run-a/checker-v3/response.md` | Final Game Finder review: qualification policy passes at proposal level; retrieval, ordering, and explanation expectations still need work. |
| `demos/run-b/checker-v3/response.md` | Final PokeJam review: mechanism UNKNOWN because winner rejection does not establish pool rejection. |
| `validation/checker-iteration/observation.md` | Actual report-precision and scoring issues, changes, reruns, and remaining interpretation limits. |
| `validation/unrelated-task/` | Arithmetic control returned 391, without loading the checker or calling history. |
| `validation/session-summary.json` | Actual call counts, skill reads, unique thread IDs, transcript hashes, and integrity checks. |

The Game Finder producer started with history-v1 loaded in its process; the
PokeJam producer started after the retrieval correction. Neither count of tests
nor a proposal establishes that a live application was fixed.

Final verification: 15 automated tests passed, the final skill passed format
validation, and all seven original source hashes remained unchanged. The two
producer sessions made 30 and 6 actual MCP calls respectively; each of the six
fresh checker sessions made 6. Every recorded session completed successfully and
preserved its protected inputs. The initial discovery and one-record transport
probe are separate from these demonstration counts.

`scripts/summarize_runs.py` builds the evidence index from the actual JSONL
events. It splits only LF records because JSON strings can contain literal
Unicode paragraph separators from the logs. Full transcripts remain unedited.

## Sources inspected / attribution

- [HW8 assignment](https://www.cs.cmu.edu/~113/hw8.html): checker/report-only
  pattern, separated review sessions, demonstration and iteration requirements.
- [Agent Skills specification](https://agentskills.io/specification): folder
  structure and required frontmatter.
- [Official Codex skill documentation](https://learn.chatgpt.com/docs/build-skills):
  local discovery directories and supported symlinks.
- [Official Codex MCP documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli):
  stdio configuration. Local `codex exec --help` verified supported CLI flags.
- [Official MCP server guide](https://modelcontextprotocol.io/docs/2026-07-28/develop/build-server):
  `MCPServer`, tool decorators, stdio transport, and stderr diagnostics. The
  installed SDK source was inspected for `ToolError` and annotation names.
- The bundled OpenAI `skill-creator` and `openai-docs` skills were read. The
  skill-creator validation script was inspected and run; it requires PyYAML
  (`requirements-dev.txt`). No third-party skill was installed. The checker
  adapts the assignment's fixed-report/citation idea to this user's examples,
  uncertainty about intent, and evidence for general fixes.

## Questions reserved for the human write-up

- Which two or three historical excerpts best explain why you want this toolkit?
- Which checker findings do you agree with, and which would you change?
- How would you explain the observed retrieval failure and revision in your words?
- What remains unproven after reviewing proposals rather than running the apps?
- Which setup steps would future-you need to reproduce it?

On November 11, the user requested concise documentation drafts. AI-assisted
`README.md`, `DEMONSTRATION.md`, and `ITERATION.md` now exist, with explicit
authorship notes. The demonstration draft records the user's actual agreement
with the main findings from the review conversation. The assignment's requirement
for student-authored final documents still applies; these drafts need the user's
review and revision before submission.
