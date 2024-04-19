@echo off
title pybrowse v3 Installer (nonadmin)
echo.
echo Welcome to the pybrowse Browser version 3 installer!
echo.
echo Working...
echo.
echo Please install Python (Python install window should open now)
echo.
start "" %USERPROFILE%/Documents/pybrowse/files/pyinstall.exe
echo When installed,
timeout /t -1
cls
echo Now installing dependencies...
echo.
echo INFO: When an error occurs here, Python is most likely not installed correctly/deprecated.
start "" %USERPROFILE%/Documents/pybrowse/files/dependencies.bat
echo.
echo When installed,
timeout /t -1
cls
echo pybrowse should now be installed correctly.
pause