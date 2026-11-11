import json
from pathlib import Path
import sys
import unittest

from mcp.client import Client
from mcp.client.stdio import StdioServerParameters


class TransportTests(unittest.IsolatedAsyncioTestCase):
    async def test_stdio_listing_search_and_error(self):
        server = Path(__file__).resolve().parents[1]/'server/history_server.py'
        async with Client(StdioServerParameters(command=sys.executable, args=[str(server)])) as client:
            listing = await client.list_tools()
            self.assertEqual([tool.name for tool in listing.tools], ['search_prompt_history'])
            result = await client.call_tool('search_prompt_history', {'query':'pump faking', 'project':'pokejam'})
            self.assertFalse(result.is_error)
            payload = json.loads(result.content[0].text)
            self.assertTrue(any('pump faking' in r['text'] for r in payload['results']))
            bad = await client.call_tool('search_prompt_history', {'query':'test', 'project':'../../'})
            self.assertTrue(bad.is_error)
            self.assertIn('unknown project', bad.content[0].text)
