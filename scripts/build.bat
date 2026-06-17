@echo off
setlocal

echo Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo Building NeuraFind...
python -m PyInstaller ^
  --name NeuraFind ^
  --windowed ^
  --icon assets\NeuraFind.ico ^
  --add-data "assets;assets" ^
  --add-data "models\minilm-onnx;models\minilm-onnx" ^
  --paths . ^
  src\neurafind\app.py

echo.
echo Build finished.
echo Output: dist\NeuraFind\NeuraFind.exe

endlocal