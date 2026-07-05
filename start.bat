@echo off
echo Starting FastAPI Backend API Server...
start python app.py

echo Starting React Frontend Dev Server...
cd frontend
npm run dev
