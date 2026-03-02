@echo off
title Nexa Run - System Check
color 0b


>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' ( goto UACPrompt ) else ( goto gotAdmin )
:UACPrompt
    echo [!] Requesting Admin Privileges...
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs" & exit /B
:gotAdmin
pushd "%CD%" & CD /D "%~dp0"

cls
echo  __________________________________________________
echo ^|                                                  ^|
echo ^|             NEXA HYPER SYSTEM V1.0               ^|
echo ^|          "System Integrity Checker"              ^|
echo ^|__________________________________________________^|
echo.


echo [*] Checking Python Installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ ERROR: PYTHON NOT FOUND ]
    echo --------------------------------------------------
    echo Python is not installed or not added to PATH.
    echo Please install Python 3.9+ from: https://www.python.org/
    echo NOTE: Make sure to check "Add Python to PATH" during setup.
    echo --------------------------------------------------
    pause
    exit
)
echo [OK] Python is ready.


echo [*] Checking Npcap Driver...
if not exist "%SystemRoot%\System32\drivers\npcap.sys" (
    echo.
    echo [ ERROR: NPCAP NOT FOUND ]
    echo --------------------------------------------------
    echo Npcap driver is required for network packet injection.
    echo Please download and install Npcap from: https://npcap.com/
    echo --------------------------------------------------
    pause
    exit
)
echo [OK] Npcap is ready.

echo.
echo [*] Checking and Installing Library Dependencies...
python -m pip install --upgrade pip >nul
python -m pip install customtkinter psutil scapy pillow >nul

if %errorlevel% neq 0 (
    echo.
    echo [!] Failed to install libraries. Check your internet connection.
    pause
    exit
)


echo.
echo [!] Optimizing TCP Stack...
netsh int tcp set global autotuninglevel=disabled >nul
netsh int ip reset >nul
echo [!] Cleaning ARP Cache...
arp -d * >nul 2>&1

echo.
echo [OK] Launching NEXA HYPER...
start pythonw nexahyper.py

exit
