@echo off
chcp 65001 >nul
title Renault Espace V (2.0 Blue dCi & Easy Link) - CAN / UDS Explorer

echo ============================================================================
echo   RENAULT ESPACE V (PHASE 2 - 2.0 Blue dCi ^& EASY LINK) - CAN / UDS SCANNER
echo ============================================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH Windows.
    echo Telechargez Python sur https://www.python.org/downloads/
    pause
    exit /b 1
)

python -c "import serial" >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Installation automatique de pyserial...
    pip install pyserial
)

echo [1] Detection des ports COM Bluetooth sur ce PC Windows :
echo ----------------------------------------------------------------------------
python scan_espace5.py --list-ports
echo ----------------------------------------------------------------------------
echo.
echo Entrez le port COM de votre Vgate iCar Pro BLE (ex: COM4)
echo ou appuyez directement sur ENTREE pour lancer une SIMULATION complete :
set /p USER_PORT="Port COM (ou vide pour simulation) > "

if not exist reports mkdir reports

if "%USER_PORT%"=="" (
    echo.
    echo [MODE SIMULATION] Lancement du scan UDS simule...
    python scan_espace5.py --simulate --md-out reports\espace5_simulation.md --json-out reports\espace5_simulation.json
) else (
    echo.
    echo [MODE REEL] Connexion au Vgate iCar Pro BLE sur %USER_PORT%...
    python scan_espace5.py --port %USER_PORT% --md-out reports\espace5_scan.md --json-out reports\espace5_scan.json
)

echo.
echo Termine ! Les rapports ont ete sauvegardes dans le dossier "reports\".
pause
