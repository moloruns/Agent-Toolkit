"""Capture a fresh Codex session, its prompt, config, and unedited JSONL events.

Usage: .venv/bin/python scripts/run_session.py <output-directory> <prompt-file>
Directories must not already contain events.jsonl. Uses the user's configured
model and Codex automatic approval review; no bypass flags or global edits.
"""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    destination = Path(sys.argv[1]).resolve()
    prompt = Path(sys.argv[2]).read_text()
    destination.mkdir(parents=True, exist_ok=True)
    if (destination / "events.jsonl").exists():
        raise SystemExit("Refusing to overwrite an existing transcript")
    (destination / "prompt.txt").write_text(prompt)
    command = [shutil.which("codex") or "codex", "exec", "--ephemeral", "--json", "--approve-for-me",
               "-C", str(ROOT), "-c", f'mcp_servers.prompt_history.command={json.dumps(str(ROOT / ".venv/bin/python"))}',
               "-c", f'mcp_servers.prompt_history.args={json.dumps([str(ROOT / "server/history_server.py")])}',
               "-o", str(destination / "response.md"), "-"]
    # Values are subprocess arguments, never interpolated into a shell.
    protected = list((ROOT / 'hw8_handoff').rglob('*')) + list((ROOT / 'skills').rglob('*'))
    if 'checker' in destination.name:
        protected += list((ROOT/'demos').rglob('proposal.md')) + list((ROOT/'demos').rglob('cases.json'))
    before = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected if p.is_file()}
    metadata = {"command": command, "fresh_session": True, "model": "inherited from user config; see events",
                "protected_before": before,
                "server_before": {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (ROOT/'server').glob('*') if p.is_file()}}
    (destination / 'session.json').write_text(json.dumps(metadata, indent=2) + '\n')
    with (destination / 'events.jsonl').open('w') as output, (destination / 'stderr.txt').open('w') as errors:
        result = subprocess.run(command, input=prompt, text=True, stdout=output, stderr=errors)
    metadata['exit_code'] = result.returncode
    metadata['protected_unchanged'] = all((ROOT/p).exists() and hashlib.sha256((ROOT/p).read_bytes()).hexdigest() == h for p,h in before.items())
    (destination / 'session.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(json.dumps({"directory": str(destination), "exit_code": result.returncode,
                      "protected_unchanged": metadata['protected_unchanged']}))
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
