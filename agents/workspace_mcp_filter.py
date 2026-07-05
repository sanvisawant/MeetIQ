# Google Workspace MCP Server Proxy/Filter
# Wraps the npm server to ensure stdout only contains valid JSON-RPC messages.

import sys
import os
import subprocess
import threading
import json

def pipe_stream(src, dest, filter_json=False):
    """Pipes text line-by-line from src to dest. Filters out non-JSON lines from stdout if enabled."""
    try:
        for line in src:
            if not line:
                continue
            if filter_json:
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    # Attempt to parse as JSON to verify JSON-RPC conformity
                    json.loads(stripped)
                    dest.write(line)
                    dest.flush()
                except ValueError:
                    # Redirect non-JSON logs (e.g. "Waiting for authentication...") to stderr so client doesn't crash
                    sys.stderr.write(f"[Workspace MCP Log] {line}")
                    sys.stderr.flush()
            else:
                dest.write(line)
                dest.flush()
    except Exception as e:
        sys.stderr.write(f"[Proxy Error] Stream pipe exception: {e}\n")
        sys.stderr.flush()

def main():
    # Use npx to launch the actual Google Workspace MCP server subprocess
    # We specify shell=True on Windows to resolve the npx command path correctly
    proc = subprocess.Popen(
        ["npx", "-y", "@presto-ai/google-workspace-mcp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        shell=True
    )

    # Spawn threads to handle bi-directional streaming
    t_in = threading.Thread(target=pipe_stream, args=(sys.stdin, proc.stdin), daemon=True)
    t_out = threading.Thread(target=pipe_stream, args=(proc.stdout, sys.stdout, True), daemon=True)
    t_err = threading.Thread(target=pipe_stream, args=(proc.stderr, sys.stderr), daemon=True)

    t_in.start()
    t_out.start()
    t_err.start()

    proc.wait()

if __name__ == "__main__":
    main()
