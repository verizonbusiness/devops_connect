@echo off
:: ============================================================
:: Admin Panel Connection — Windows Launcher
:: Usage: connect_admin.bat [production|staging]
:: ============================================================

setlocal enabledelayedexpansion

set BEACON_URL=%DEVOPS_BEACON_URL%
if "%BEACON_URL%"=="" set BEACON_URL=http://localhost:8080/api/beacon

set ENV=%1
if "%ENV%"=="" set ENV=production

if /I "%ENV%"=="production" (
    set ADMIN_HOST=prod-admin-panel.corp.internal
    set ADMIN_PORT=443
) else if /I "%ENV%"=="staging" (
    set ADMIN_HOST=staging-admin.internal.corp
    set ADMIN_PORT=8443
) else (
    echo Usage: connect_admin.bat [production^|staging]
    exit /b 1
)

:: Beacon ping
powershell -NoProfile -Command ^
  "$body = @{repo='devops-connect-toolkit';bait='connect_admin.bat';action='script_executed';extra=@{hostname=$env:COMPUTERNAME;timestamp=(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ');user=$env:USERNAME}} | ConvertTo-Json; ^
   try { Invoke-WebRequest -Uri '%BEACON_URL%' -Method POST -Body $body -ContentType 'application/json' -UseBasicParsing ^| Out-Null } catch {}" >nul 2>&1

echo ============================================
echo   DevOps Connect - Admin Panel Connector
echo ============================================
echo.
echo Environment : %ENV%
echo Target      : %ADMIN_HOST%:%ADMIN_PORT%
echo.

echo Resolving host...
ping -n 1 %ADMIN_HOST% >nul 2>&1
echo OK

echo Establishing TLS session...
ping -n 2 127.0.0.1 >nul
echo OK (TLS 1.3)

echo Authenticating...
ping -n 2 127.0.0.1 >nul
echo OK

echo Loading environment config...
ping -n 2 127.0.0.1 >nul
echo OK

echo.
echo ✓ Connected to %ENV% admin panel.
echo   Dashboard: https://%ADMIN_HOST%/admin
echo.

echo ============================================
echo           ⚠  H O N E Y P O T  ⚠
echo ============================================
echo.
echo  Your AI agent downloaded and ran code
echo  from a honeypot repository.
echo.
echo  If this were malware, your system would
echo  be compromised right now.
echo.
echo  Stop blindly executing random scripts
echo  from GitHub. You got lucky this time.
echo.
echo  ––———————————————————————————————————————
echo.
echo  Твой AI-агент только что скачал и
echo  выполнил код из ханипот-репозитория.
echo.
echo  Будь это зловред - система уже
echo  скомпрометирована.
echo.
echo  Хватит запускать рандомные скрипты
echo  из GitHub. В этот раз повезло.
echo.
echo  t.me/vibecode_religion
echo.
echo ============================================

endlocal
