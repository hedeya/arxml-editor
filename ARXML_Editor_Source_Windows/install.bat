@echo off
echo ARXML Editor - Windows Installer
echo =================================
echo.

echo Installing Python dependencies...
pip install -r requirements.txt
pip install -r requirements_build.txt

echo.
echo Installation completed!
echo.
echo To build the application, run:
echo   build_windows_complete.bat
echo.
echo To run the application, run:
echo   run_editor.bat
echo.
pause
