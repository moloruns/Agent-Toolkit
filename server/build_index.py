"""Rebuild the in-memory index and print its coverage for inspection."""
import json
from history import HistoryIndex

if __name__ == "__main__":
    index = HistoryIndex()
    print(json.dumps(index.coverage(), indent=2))
    index.close()
