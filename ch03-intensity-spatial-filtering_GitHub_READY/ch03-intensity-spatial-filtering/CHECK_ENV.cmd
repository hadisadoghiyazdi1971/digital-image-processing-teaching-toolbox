@echo off
setlocal
cd /d "%~dp0"

echo ================================================================
echo Chapter 3 Toolbox - Python 3.12 environment check
echo ================================================================

py -3.12 -c "import sys; print('Python:', sys.version); print('Executable:', sys.executable)"
if errorlevel 1 goto :no312

echo.
py -3.12 -c "import numpy; print('numpy       ', numpy.__version__)"
py -3.12 -c "import scipy; print('scipy       ', scipy.__version__)"
py -3.12 -c "import skimage; print('scikit-image', skimage.__version__)"
py -3.12 -c "import PIL; print('Pillow      ', PIL.__version__)"
py -3.12 -c "import matplotlib; print('matplotlib  ', matplotlib.__version__)"
py -3.12 -c "import tkinter; print('tkinter      OK')"

echo.
echo If all lines above printed a version/OK, run RUN_TOOLBOX.cmd
pause
exit /b 0

:no312
echo.
echo [ERROR] Python 3.12 was not found through the Windows py launcher.
echo Install Python 3.12 or run: py -0p
pause
exit /b 1
