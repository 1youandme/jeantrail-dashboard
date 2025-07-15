@echo off
cd /d C:\Users\dell\JeanTrail_AI\backend_fastapi

:: تشغيل السيرفر في نافذة منفصلة
start "Uvicorn Server" cmd /k "C:\Users\dell\AppData\Local\Programs\Python\Python313\python.exe -m uvicorn main:app --reload"

:: الانتظار 10 ثواني لضمان تشغيل السيرفر
timeout /t 10 /nobreak

:: تشغيل test_supabase.py
C:\Users\dell\AppData\Local\Programs\Python\Python313\python.exe test_supabase.py

pause
