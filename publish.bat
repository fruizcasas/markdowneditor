@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
title Publish MarkdownEditor

echo.
echo ============================================================
echo    MARKDOWN EDITOR - Publish distribution / Publicar distribucion
echo ============================================================
echo.

REM Verify src exists / Verificar que existe src
if not exist "src" (
    echo ERROR: src/ folder does not exist / La carpeta src/ no existe
    pause
    exit /b 1
)

REM Create dist folder if not exists / Crear carpeta dist si no existe
if not exist "dist" mkdir dist

REM Generate name with date and time: md_editor_YYMMDD_HHmm.zip
REM Generar nombre con fecha y hora: md_editor_YYMMDD_HHmm.zip
for /f "tokens=1-5 delims=/:. " %%a in ("%date% %time%") do (
    set "YEAR=%%c"
    set "MONTH=%%b"
    set "DAY=%%a"
    set "HOUR=%%d"
    set "MIN=%%e"
)

REM Adjust format (may vary by regional settings)
REM Ajustar formato (puede variar segun configuracion regional)
set "YEAR=%YEAR:~-2%"
set "ZIPNAME=md_editor_%YEAR%%MONTH%%DAY%_%HOUR%%MIN%.zip"

echo   Generating / Generando: dist\%ZIPNAME%
echo.

REM Create temp folder for zip content / Crear carpeta temporal para contenido del zip
set "TEMPDIR=%TEMP%\MarkdownEditor_publish"
if exist "%TEMPDIR%" rmdir /s /q "%TEMPDIR%"
mkdir "%TEMPDIR%\MarkdownEditor"

REM Copy files / Copiar archivos
echo   Copying files... / Copiando archivos...

copy "src\1_Install.bat" "%TEMPDIR%\MarkdownEditor\" >nul
copy "src\MarkdownEditor.bat" "%TEMPDIR%\MarkdownEditor\" >nul
copy "src\README.txt" "%TEMPDIR%\MarkdownEditor\" >nul

REM Copy bin/ with main.py and modules/ / Copiar bin/ con main.py y modules/
xcopy /E /I /Q "src\bin" "%TEMPDIR%\MarkdownEditor\bin" >nul

REM Copy styles/ / Copiar styles/
xcopy /E /I /Q "src\styles" "%TEMPDIR%\MarkdownEditor\styles" >nul

REM Create empty wkhtmltopdf folder / Crear carpeta wkhtmltopdf vacia
mkdir "%TEMPDIR%\MarkdownEditor\wkhtmltopdf"

echo   Creating ZIP... / Creando ZIP...

REM Use PowerShell to create zip / Usar PowerShell para crear zip
powershell -NoProfile -Command "Compress-Archive -Path '%TEMPDIR%\MarkdownEditor' -DestinationPath 'dist\%ZIPNAME%' -Force"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Could not create ZIP / No se pudo crear el ZIP
    echo Verify PowerShell is available / Verifica que PowerShell este disponible
    pause
    exit /b 1
)

REM Clean temp / Limpiar temporal
rmdir /s /q "%TEMPDIR%"

echo.
echo ============================================================
echo   Published / Publicado: dist\%ZIPNAME%
echo ============================================================
echo.
echo   User extracts and gets: / El usuario descomprime y obtiene:
echo.
echo   MarkdownEditor\
echo       1_Install.bat
echo       MarkdownEditor.bat
echo       README.txt
echo       bin\
echo           main.py
echo           modules\
echo               app.py, config.py, etc.
echo       styles\
echo       wkhtmltopdf\
echo.

REM Open dist folder / Abrir carpeta dist
explorer "dist"

pause
