Write-Host "Starting FastAPI Backend API Server..." -ForegroundColor Cyan
Start-Process python -ArgumentList "app.py"

Write-Host "Starting React Frontend Dev Server..." -ForegroundColor Green
Set-Location frontend
npm run dev
