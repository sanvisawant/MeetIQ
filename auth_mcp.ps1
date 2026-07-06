# Helper script to perform one-time Google Workspace MCP Authentication
# It points to the local .mcp-credentials directory to persist your login credentials.

$project_root = Resolve-Path "."
$env:GOOGLE_WORKSPACE_MCP_HOME = Join-Path $project_root ".mcp-credentials"

Write-Host "---------------------------------------------------------" -ForegroundColor Yellow
Write-Host "Starting Google Workspace MCP Authentication..." -ForegroundColor Cyan
Write-Host "If a browser window does not open automatically, look for" -ForegroundColor Green
Write-Host "an OAuth URL in the output below and copy it to your browser." -ForegroundColor Green
Write-Host "---------------------------------------------------------" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to exit once you have successfully signed in." -ForegroundColor Cyan
Write-Host ""

npx -y @presto-ai/google-workspace-mcp --auth
