@echo off
chcp 65001 >nul
title Installation Miroir Android Auto (Fermata Mirror) - Renault Espace V Easy Link

echo ============================================================================
echo   INSTALLATION DU MIROIR D'ECRAN ANDROID AUTO (FERMATA MIRROR / FS MIRROR)
echo   Pour Ecran 9.3" Easy Link - Renault Espace V (Signature Play Store ADB)
echo ============================================================================
echo.

where adb >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERREUR] L'outil 'adb' ^(Android Debug Bridge^) n'est pas dans le PATH Windows.
    echo Telechargez Android Platform Tools : https://developer.android.com/tools/releases/platform-tools
    pause
    exit /b 1
)

echo [1] Verification de la connexion ADB avec votre smartphone Android...
adb devices
echo.
echo Assurez-vous que le "Debogage USB" est active sur votre telephone et autorise.
echo.

set APK_PATH=%1
if "%APK_PATH%"=="" (
    echo Pour installer un APK ^(ex: fermata-auto.apk^) avec la signature Play Store
    echo requise par Android Auto ^(com.android.vending^), glissez-deposez le fichier
    echo APK sur ce script ou entrez son chemin complet ci-dessous :
    set /p APK_PATH="Chemin du fichier .apk > "
)

if "%APK_PATH%"=="" (
    echo Aucun fichier APK specifie. Fin du script.
    pause
    exit /b 1
)

echo.
echo [2] Installation de %APK_PATH% avec l'identifiant d'installateur Play Store ^(com.android.vending^)...
adb install -r -i "com.android.vending" "%APK_PATH%"

if %errorlevel% equ 0 (
    echo.
    echo [SUCCES] Application installee avec la signature Play Store !
    echo N'oubliez pas d'activer "Sources inconnues" dans les Parametres Developpeur d'Android Auto.
) else (
    echo.
    echo [ERREUR] L'installation ADB a echoue. Verifiez que le telephone est bien deverrouille.
)

pause
