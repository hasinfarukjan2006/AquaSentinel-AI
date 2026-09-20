@echo off
echo Starting JalRakshak React Frontend Dashboard...
cd frontend
set "PATH=C:\Users\dellc\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin;C:\Users\dellc\.cache\codex-runtimes\codex-primary-runtime\dependencies\node;%PATH%"
"C:\Users\dellc\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" node_modules/vite/bin/vite.js
pause
