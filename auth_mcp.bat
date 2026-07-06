@echo off
rem Helper script to perform one-time Google Workspace MCP Authentication
rem It points to the local .mcp-credentials directory to persist your login credentials.

set "GOOGLE_WORKSPACE_MCP_HOME=%CD%\.mcp-credentials"

echo ---------------------------------------------------------
echo Starting Google Workspace MCP Authentication...
echo If a browser window does not open automatically, look for
echo an OAuth URL in the output below and copy it to your browser.
echo ---------------------------------------------------------
echo Press Ctrl+C to exit once you have successfully signed in.
echo.

npx -y @presto-ai/google-workspace-mcp --auth
