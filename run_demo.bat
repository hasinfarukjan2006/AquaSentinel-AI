@echo off
echo ========================================================
echo JALRAKSHAK AI — ONE-COMMAND DEMO LAUNCHER
echo Tagline: "From Water Risk to Early Action."
echo ========================================================
echo.
echo 1. Initializing SQLite Database & Risk Scoring Engine...
"C:\Users\dellc\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" database/init_db.py

echo.
echo 2. Launching Flask REST API Backend (Port 5000)...
start "JalRakshak Backend API" "C:\Users\dellc\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" backend/app.py

echo.
echo 3. Launching React Frontend Dashboard (Port 5173)...
cd frontend
set "PATH=C:\Users\dellc\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin;C:\Users\dellc\.cache\codex-runtimes\codex-primary-runtime\dependencies\node;%PATH%"
start "JalRakshak Frontend UI" "C:\Users\dellc\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" node_modules/vite/bin/vite.js --host 0.0.0.0 --port 5173

echo.
echo JalRakshak AI prototype launched successfully!
echo Backend API: http://localhost:5000/api/health
echo Frontend Dashboard: http://localhost:5173
echo ========================================================
pause
