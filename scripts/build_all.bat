@echo off
setlocal

echo ==============================================
echo 1. Cleaning old build files...
echo ==============================================
if exist build rmdir /s /q build
if exist dist\NeuraFind rmdir /s /q dist\NeuraFind

echo.
echo ==============================================
echo 2. Building NeuraFind with PyInstaller...
echo ==============================================
python -m PyInstaller ^
  --name NeuraFind ^
  --windowed ^
  --icon assets\NeuraFind.ico ^
  --add-data "assets;assets" ^
  --add-data "models\minilm-onnx;models\minilm-onnx" ^
  --paths . ^
  src\neurafind\app.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] PyInstaller build failed!
    exit /b %ERRORLEVEL%
)

echo.
echo ==============================================
echo 3. Creating Setup Installer with Inno Setup...
echo ==============================================

rem Check common installation paths for Inno Setup
set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %ISCC% (
    set ISCC="C:\Program Files\Inno Setup 6\ISCC.exe"
)

if not exist %ISCC% (
    echo.
    echo [WARNING] Inno Setup compiler ^(ISCC.exe^) not found.
    echo Please install Inno Setup 6 from https://jrsoftware.org/isdl.php
    echo The PyInstaller build is complete in dist\NeuraFind, but the Setup.exe was not created.
    exit /b 1
)

%ISCC% scripts\installer_script.iss

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Inno Setup compilation failed!
    exit /b %ERRORLEVEL%
)

echo.
echo ==============================================
echo 4. Cleaning up intermediate portable files...
echo ==============================================
rmdir /s /q dist\NeuraFind

echo.
echo ==============================================
echo Build finished successfully!
echo Setup file is located in: dist\NeuraFind_Setup_v1.0.0.exe
echo ==============================================

endlocal
