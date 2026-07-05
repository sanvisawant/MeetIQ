#!/bin/bash
echo "Starting FastAPI Backend API Server..."
python app.py &

echo "Starting React Frontend Dev Server..."
cd frontend
npm run dev
