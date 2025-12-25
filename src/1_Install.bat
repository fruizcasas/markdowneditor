@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
title Markdown Editor - Installation / Instalacion

echo.
echo ============================================================
echo         MARKDOWN EDITOR - Installation / Instalacion
echo ============================================================
echo.

REM =============================================================================
REM CONFIGURATION - EDIT HERE IF PYTHON IS NOT DETECTED
REM CONFIGURACION - EDITA AQUI SI PYTHON NO SE DETECTA
REM =============================================================================
REM Uncomment and edit this line with your Python path:
REM Descomenta y edita esta linea con la ruta de tu Python:
REM set PYTHON_PATH=C:\Users\YOUR_USER\AppData\Local\Programs\Python\Python311\python.exe
REM =============================================================================

if defined PYTHON_PATH (
    echo [INFO] Using configured Python / Usando Python configurado: %PYTHON_PATH%
    set PYTHON_CMD=%PYTHON_PATH%
    goto :check_python_exists
)

echo [1/3] Searching for Python... / Buscando Python...
echo.

REM Search in PATH / Buscar en PATH
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
    echo       Found / Encontrado: python
    goto :check_python_version
)

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=py
    echo       Found / Encontrado: py launcher
    goto :check_python_version
)

REM Search in common locations / Buscar en ubicaciones comunes
if exist "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" (
    set "PYTHON_CMD=%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe"
    echo       Found / Encontrado: WindowsApps
    goto :check_python_version
)

if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    set "PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    echo       Found / Encontrado: Python313
    goto :check_python_version
)

if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    echo       Found / Encontrado: Python312
    goto :check_python_version
)

if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set "PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    echo       Found / Encontrado: Python311
    goto :check_python_version
)

if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    set "PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    echo       Found / Encontrado: Python310
    goto :check_python_version
)

goto :python_not_found

:check_python_exists
if not exist "%PYTHON_CMD%" (
    echo [ERROR] Configured path does not exist / La ruta configurada no existe: %PYTHON_CMD%
    goto :python_not_found
)

:check_python_version
echo.
echo [2/3] Verifying Python... / Verificando Python...
"%PYTHON_CMD%" --version
if %ERRORLEVEL% NEQ 0 goto :python_not_found

REM Save path for MarkdownEditor.bat / Guardar ruta para MarkdownEditor.bat
echo set PYTHON_CMD=%PYTHON_CMD%> "%~dp0_python_path.bat"

REM Install dependencies / Instalar dependencias
echo.
echo [3/3] Installing dependencies (1-2 minutes)... / Instalando dependencias (1-2 minutos)...
echo.

"%PYTHON_CMD%" -m pip install --upgrade pip >nul 2>&1

echo       - customtkinter
"%PYTHON_CMD%" -m pip install customtkinter
if %ERRORLEVEL% NEQ 0 goto :pip_error

echo       - markdown
"%PYTHON_CMD%" -m pip install markdown
if %ERRORLEVEL% NEQ 0 goto :pip_error

echo       - pygments
"%PYTHON_CMD%" -m pip install pygments
if %ERRORLEVEL% NEQ 0 goto :pip_error

echo       - tkinterweb
"%PYTHON_CMD%" -m pip install tkinterweb
if %ERRORLEVEL% NEQ 0 goto :pip_error

echo       - pyperclip
"%PYTHON_CMD%" -m pip install pyperclip
if %ERRORLEVEL% NEQ 0 goto :pip_error

echo       - tkinterdnd2 (drag and drop)
"%PYTHON_CMD%" -m pip install tkinterdnd2
if %ERRORLEVEL% NEQ 0 goto :pip_error

echo       - windnd (native drag and drop / arrastrar y soltar nativo)
"%PYTHON_CMD%" -m pip install windnd
if %ERRORLEVEL% NEQ 0 goto :pip_error

echo.
echo ============================================================
echo     INSTALLATION COMPLETED / INSTALACION COMPLETADA
echo ============================================================
echo.
echo   You can now run / Ya puedes ejecutar: MarkdownEditor.bat
echo.
echo   (This installer is no longer needed, you can delete it)
echo   (Este instalador ya no es necesario, puedes borrarlo)
echo.
pause
exit /b 0

:python_not_found
echo.
echo ============================================================
echo          PYTHON NOT FOUND / PYTHON NO ENCONTRADO
echo ============================================================
echo.
echo   Options / Opciones:
echo.
echo   A) Configure path manually / Configurar ruta manualmente:
echo      1. Open this file with Notepad / Abre este archivo con Bloc de notas
echo      2. Find "set PYTHON_PATH=" / Busca "set PYTHON_PATH="
echo      3. Uncomment and set your path / Descomenta y pon tu ruta
echo      4. Save and run again / Guarda y ejecuta de nuevo
echo.
echo   B) Install Python without admin / Instalar Python sin admin:
echo      1. Download from / Descarga de: https://www.python.org/downloads/
echo      2. Run installer / Ejecuta el instalador
echo      3. Select "Customize installation"
echo      4. Check "Install for current user only"
echo.
pause
exit /b 1

:pip_error
echo.
echo [ERROR] Installation failed. Check Internet connection.
echo [ERROR] Fallo la instalacion. Verifica conexion a Internet.
echo.
pause
exit /b 1
