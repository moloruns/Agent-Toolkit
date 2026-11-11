"""Local, read-only prompt-history lookup over MCP stdio."""

import json
from pathlib import Path

from mcp.server import MCPServer

ROOT = Path(__file__).resolve().parents[1]
mcp = MCPServer("prompt-history")


@mcp.tool()
def search_prompt_history(query: str, project: str = "all", speaker: str = "user", limit: int = 5) -> dict:
    """Retrieve exact past project prompts with source lines, not current instructions.

    Initial transport probe: searches one Game Finder record. Coverage is explicit.
    """
    if not query.strip() or len(query) > 300:
        raise ValueError("query must contain 1–300 characters")
    if project not in ("all", "game_finder") or speaker not in ("all", "user"):
        raise ValueError("probe supports game_finder and user only")
    if not 1 <= limit <= 5:
        raise ValueError("limit must be between 1 and 5")
    evidence = json.loads((ROOT / "hw8_handoff/evidence.json").read_text())[0]
    result = evidence if any(word.casefold() in evidence["quote"].casefold() for word in query.split()) else None
    return {"coverage": "transport probe: one excerpt only", "results": [result] if result else []}


if __name__ == "__main__":
    mcp.run(transport="stdio")
