# Fix the Pattern — Agent Toolkit


This toolkit helps an agent understand the problem behind a user's examples. It combines a checker skill with an MCP tool that searches past project conversations.

The motivation came from Game Finder and PokeJam. Their examples exposed broader issues with recommendations and comparisons: matching one part of a request, or being the closest available result, was not always enough.

## What it does

- **`fix-the-pattern` skill:** reviews a proposed or implemented fix for underlying intent, a general mechanism, varied cases, and claims supported by evidence. It reports findings without editing the work. Use it when checking whether a fix addresses the broader problem behind reported examples.
- **`search_prompt_history` MCP tool:** searches seven HW3–7 logs and returns exact excerpts, speaker attribution, source lines, and bounded context. It gives new sessions structured access to earlier decisions and corrections.

The skill defines how to review. The MCP server supplies the history used during that review. Reviews should run in a fresh session separate from the agent that produced the work.

## Why these tools

In Game Finder, the author explicitly corrected the focus of the work:

> Don't just fix specific examples, but look at the model itself, then see how the app outputs.

Source: [Game Finder log, line 416](hw8_handoff/logs/hw6_game_finder.md#L416).

The need for portable history appeared in PokeJam:

> okay, now put everything we've done now (including a run down of what this is), along with the next phases for revision4 in a file called "next steps". I am about to deploy another agent to move on with this phase.

Source: [PokeJam log, line 548](hw8_handoff/logs/hw5_pokejam.txt#L548). More excerpts and their context are in the [evidence guide](hw8_handoff/evidence.md).

## Installation

These instructions use macOS/Linux shell commands. The tested setup was macOS arm64, Python 3.13.7, MCP SDK 2.3.0, and Codex CLI 0.162.0-alpha.17.2. Other clients have not been separately verified.

From the downloaded or cloned repository's root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python server/build_index.py
.venv/bin/python -m unittest discover -s tests -v
```

The index command verifies the source files and prints search coverage. The saved test run passed all 15 tests. The server rebuilds its small in-memory index when it starts; it needs no embedding service or API key.

### Load the skill

This checkout includes `.agents/skills/fix-the-pattern`, linked to [the skill folder](skills/fix-the-pattern/SKILL.md). For another repository, copy `skills/fix-the-pattern` into that repository's `.agents/skills/` directory. A user-wide installation can go in `~/.agents/skills/`.

### Register the MCP server

Add this table to `~/.codex/config.toml`, preserving other settings. Replace **both** `/ABSOLUTE/PATH/Agent-Toolkit` placeholders with the actual checkout path. This configuration is also provided in [config/codex.example.toml](config/codex.example.toml).

```toml
[mcp_servers.prompt_history]
command = "/ABSOLUTE/PATH/Agent-Toolkit/.venv/bin/python"
args = ["/ABSOLUTE/PATH/Agent-Toolkit/server/history_server.py"]
```

Start a new Codex session and ask:

> Use search_prompt_history to search for "specific examples" in game_finder, and show the source location.

Confirm that an actual MCP tool call appears. To review work, start a separate fresh session and ask:

> Use $fix-the-pattern to review demos/run-a/proposal.md and demos/run-a/cases.json. Use the history tool to recover the relevant intent. Report findings without changing files.

## Evidence and limits

- [DEMONSTRATION.md](DEMONSTRATION.md): two real proposal tasks, MCP calls, and separate checker reviews.
- [ITERATION.md](ITERATION.md): observed checker and retrieval weaknesses, revisions, and reruns.
- [Build record](notes/build-record.md): detailed setup facts and links to raw evidence.

Search is keyword-based, not semantic. Some log attribution is uncertain and labeled `unknown`; inherited-author history is excluded from the default search. Results can be truncated, and older decisions may have later corrections. The demonstrations reviewed proposals and synthetic cases; they did not establish that the original apps were fixed.

## Sources and AI use

Codex helped plan and implement the toolkit, create tests and demonstration proposals, run separate checker sessions, and draft this documentation. The bundled `skill-creator` and `openai-docs` skills were consulted; no third-party skill was installed. The author selected the direction, emphasized understanding their intent, and agreed with the main demonstration findings. Recorded prompts, outputs, and tool calls are linked in the demonstration and iteration documents.
