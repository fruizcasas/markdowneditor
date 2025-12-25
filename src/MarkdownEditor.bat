@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

REM Check if installer exists and offer cleanup
REM Verificar si existe el instalador y ofrecer limpieza
if exist "1_Install.bat" (
    echo.
    echo ============================================================
    echo   The file 1_Install.bat still exists.
    echo   El archivo 1_Install.bat aun existe.
    echo.
    echo   If installation is complete, it's recommended to delete it
    echo   to avoid accidental reinstalls that could overwrite settings.
    echo.
    echo   Si ya completaste la instalacion, es recomendable eliminarlo
    echo   para evitar reinstalaciones que sobrescriban configuraciones.
    echo ============================================================
    echo.
    choice /C YN /M "Delete 1_Install.bat? / Eliminar 1_Install.bat? (Y=Yes/Si, N=No)"
    if !ERRORLEVEL! EQU 1 (
        del "1_Install.bat"
        echo.
        echo   Deleted. / Eliminado.
    ) else (
        echo.
        echo   OK, keeping it. / OK, se mantiene.
    )
    echo.
)

REM Load Python path / Cargar ruta de Python
if exist "%~dp0_python_path.bat" (
    call "%~dp0_python_path.bat"
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set PYTHON_CMD=python
    ) else (
        where py >nul 2>&1
        if %ERRORLEVEL% EQU 0 (
            set PYTHON_CMD=py
        ) else (
            echo.
            echo ERROR: Python not configured. / Python no configurado.
            echo Run 1_Install.bat first. / Ejecuta primero 1_Install.bat
            echo.
            pause
            exit /b 1
        )
    )
)

REM Verify bin/main.py exists / Verificar que existe bin/main.py
if not exist "%~dp0bin\main.py" (
    echo.
    echo ERROR: bin\main.py not found / No se encuentra bin\main.py
    echo.
    pause
    exit /b 1
)

REM Run the editor / Ejecutar el editor
"%PYTHON_CMD%" "%~dp0bin\main.py"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Editor closed with errors. / El editor se cerro con errores.
    echo If first time, run 1_Install.bat / Si es la primera vez, ejecuta 1_Install.bat
    echo.
    pause
)
