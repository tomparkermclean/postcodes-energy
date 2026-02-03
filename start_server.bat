@echo off
cd /d "C:\Users\blueb\OneDrive\Documents\postcodes-energy\public"
echo Starting server from: %CD%
echo.
echo Open your browser to: http://localhost:8000
echo.
python -m http.server 8000
