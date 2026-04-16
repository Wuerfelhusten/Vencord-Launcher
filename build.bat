@echo off
REM Clean previous build and dist folders, if they exist
rmdir /s /q dist
rmdir /s /q build

uv run nuitka ^
    --standalone ^
    --output-filename=VencordLauncher.exe ^
    --windows-icon-from-ico=assets\icon.ico ^
    --remove-output ^
    src\main.py

REM Copy config.json next to the executable
copy data\config.json dist\main.dist\config.json

echo.
echo Done! VencordLauncher.exe and config.json are now in dist\main.dist\
pause
