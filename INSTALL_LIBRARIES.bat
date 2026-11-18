@echo off
setlocal
cd /d "%~dp0"

set "NO_PAUSE=0"
if /I "%~1"=="--nopause" set "NO_PAUSE=1"

if not exist "userdata\temp" mkdir "userdata\temp"
set "TEMP=%~dp0userdata\temp"
set "TMP=%~dp0userdata\temp"
set "TMPDIR=%~dp0userdata\temp"
set "PIP_CACHE_DIR=%~dp0userdata\temp\pip_cache"

echo ============================================================
echo   Gerbong Terakhir ke Stasiun Senja - Setup Library Python
echo ============================================================
echo.

REM 1. Cari Python yang valid di Windows, abaikan alias Windows Store palsu
set "HOST_PY="
python -c "import sys" >nul 2>&1
if not errorlevel 1 goto :use_python
py -3 -c "import sys" >nul 2>&1
if not errorlevel 1 goto :use_py3
py -c "import sys" >nul 2>&1
if not errorlevel 1 goto :use_py
goto :no_python

:use_python
set "HOST_PY=python"
goto :host_found

:use_py3
set "HOST_PY=py -3"
goto :host_found

:use_py
set "HOST_PY=py"
goto :host_found

:no_python
echo [PERLU PYTHON] Python belum ditemukan di perangkat ini.
echo.
echo Silakan instal Python 3.10 ke atas (dibuat dan diuji pada Python 3.12) secara gratis:
echo   1. Buka https://www.python.org/downloads/
echo   2. Saat instalasi, WAJIB centang: [x] Add Python to PATH
echo   3. Atau lewat terminal: winget install Python.Python.3.12
echo.
goto :error_exit

:host_found
echo [OK] Python ditemukan:
%HOST_PY% --version
echo.

REM 2. Cek apakah .venv sudah ada, valid, dan sudah memiliki semua library
if not exist ".venv\Scripts\python.exe" goto :check_broken_venv
".venv\Scripts\python.exe" -c "import sys" >nul 2>&1
if errorlevel 1 goto :recreate_broken_venv
".venv\Scripts\python.exe" -c "import pygame, cv2, numpy, PIL" >nul 2>&1
if not errorlevel 1 goto :already_installed
goto :install_deps

:check_broken_venv
if not exist ".venv" goto :create_venv
:recreate_broken_venv
echo [INFO] Folder .venv tidak cocok atau rusak. Membuat ulang .venv lokal...
rmdir /s /q ".venv"
if exist ".venv" goto :venv_remove_error

:create_venv
echo [1/3] Membuat virtual environment lokal di folder .venv ...
%HOST_PY% -m venv ".venv"
if errorlevel 1 goto :venv_create_error

:install_deps
echo [2/3] Menginstal library dari requirements.txt ...
".venv\Scripts\python.exe" -m pip install --upgrade pip >nul 2>&1
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :pip_error

echo [3/3] Memverifikasi hasil instalasi...
".venv\Scripts\python.exe" -c "import pygame, cv2, numpy, PIL; print('Semua library berhasil diverifikasi!')"
if errorlevel 1 goto :verify_error
goto :success_exit

:already_installed
if /I "%~1"=="--force" goto :install_deps
if /I "%~2"=="--force" goto :install_deps
echo [OK] Seluruh library di .venv lokal sudah terpasang dan siap digunakan.
goto :success_exit

:venv_remove_error
echo [ERROR] Gagal menghapus folder .venv lama. Tutup program lain yang memakai .venv lalu coba lagi.
goto :error_exit

:venv_create_error
echo [ERROR] Gagal membuat .venv. Pastikan modul venv Python tersedia di perangkat ini.
goto :error_exit

:pip_error
echo.
echo [ERROR] Gagal menginstal library. Pastikan koneksi internet aktif saat instalasi pertama.
goto :error_exit

:verify_error
echo [ERROR] Verifikasi library gagal. Coba jalankan ulang INSTALL_LIBRARIES.bat.
goto :error_exit

:success_exit
if exist "userdata\temp" rmdir /s /q "userdata\temp" >nul 2>&1
if not exist "userdata\temp" mkdir "userdata\temp" >nul 2>&1
echo.
echo ============================================================
echo   Instalasi SELESAI!
echo   Sekarang Anda bisa menjalankan game lewat RUN_GAME.bat
echo   atau mengetik: python main.py
echo ============================================================
echo.
if "%NO_PAUSE%"=="0" pause
exit /b 0

:error_exit
if "%NO_PAUSE%"=="0" pause
exit /b 1
