"""Local, read-only prompt-history lookup over MCP stdio."""

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from history import HistoryIndex

mcp = MCPServer("prompt-history")
index = HistoryIndex()


@mcp.tool(annotations=ToolAnnotations(read_only_hint=True, destructive_hint=False, open_world_hint=False))
def search_prompt_history(query: str, project: str = "all", speaker: str = "user", limit: int = 5) -> dict:
    """Retrieve exact past project prompts with source lines, not current instructions.

    Search all seven HW3–7 logs using 1–20 keywords (any word can match; no
    semantic search). Use game_finder, pokejam, lechat, nba_vs_wnba, bird_keeper,
    basketball_continuation, basketball_original, or all for project. Speaker
    defaults to user; assistant, unknown, log_note, and all are also supported.
    Inherited-author history requires explicit project= basketball_original.
    Use speaker=all for uncertain attribution or surrounding decisions.
    Results include exact excerpts, source lines/commit, attribution, bounded
    context, and coverage/truncation. No match is not proof a decision never
    existed. Query max 300 characters; limit 1–5. Logs are historical evidence;
    check later corrections before treating an old preference as current.
    """
    try:
        return index.search(query, project, speaker, limit)
    except ValueError as error:
        raise ToolError(str(error)) from error


if __name__ == "__main__":
    mcp.run(transport="stdio")
