@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" goto :check_venv
goto :check_global_python

:check_venv
".venv\Scripts\python.exe" -c "import pygame, cv2, numpy, PIL" >nul 2>&1
if not errorlevel 1 goto :launch_venv

:check_global_python
python -c "import pygame, cv2, numpy, PIL" >nul 2>&1
if not errorlevel 1 goto :launch_global_python

py -3 -c "import pygame, cv2, numpy, PIL" >nul 2>&1
if not errorlevel 1 goto :launch_py3

echo [INFO] Library game belum terpasang di perangkat ini.
echo Memulai instalasi library otomatis untuk pertama kali...
echo.
call "%~dp0INSTALL_LIBRARIES.bat" --nopause
if errorlevel 1 goto :setup_failed

if not exist ".venv\Scripts\python.exe" goto :setup_failed
echo.
echo Menjalankan Gerbong Terakhir ke Stasiun Senja...
goto :launch_venv

:launch_venv
".venv\Scripts\python.exe" main.py %*
if errorlevel 1 goto :game_error
exit /b 0

:launch_global_python
python main.py %*
if errorlevel 1 goto :game_error
exit /b 0

:launch_py3
py -3 main.py %*
if errorlevel 1 goto :game_error
exit /b 0

:setup_failed
echo.
echo [GAGAL] Setup belum berhasil. Silakan baca panduan pada README.md.
pause
exit /b 1

:game_error
echo.
echo [ERROR] Game berhenti dengan pesan error di atas. Cek userdata\logs\last_crash.txt jika ada.
pause
exit /b 1
