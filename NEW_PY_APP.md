# NEW_PY_APP.md - Guide to Create Python Applications Without Knowing Python
# NEW_PY_APP.md - Guía para Crear Aplicaciones Python Sin Saber Python

**Author/Autor:** Fernando Ruiz Casas (fruizcasas@gmail.com)  
**Assistant/Asistente:** Claude (Anthropic Opus 4.5)  
**Date/Fecha:** December 2025 / Diciembre 2025  
**License/Licencia:** MIT

---

## User Context / Contexto del Usuario

- **Profile/Perfil**: Knows programming but NOT Python / Sabe programar pero NO conoce Python
- **Environment/Entorno**: Windows 10/11, Python user-mode, VS Code user-mode
- **Claude Access/Acceso a Claude**: Multi-AI portal (text chat only, NO artifacts, NO MCP) / Portal multi-IA (solo chat texto, SIN artifacts, SIN MCP)
- **Workflow/Flujo**: Copy code from chat → Paste in VS Code → Save / Copiar código del chat → Pegar en VS Code → Guardar

---

## Enterprise Environment Restrictions / Restricciones Entorno Enterprise

| NOT allowed / NO puede | CAN do / SÍ puede |
|------------------------|-------------------|
| ❌ Install as admin / Instalar como admin | ✅ VS Code user mode |
| ❌ Global runtimes / Runtimes globales | ✅ Python user install (Microsoft Store) |
| ❌ Claude Artifacts | ✅ pip install --user |
| ❌ MCP / tools / herramientas | ✅ PowerShell with bypass / con bypass |
| ❌ Download .exe / Descargar .exe | ✅ Copy/paste from chat / Copiar/pegar desde chat |

---

## Initializer Script / Script Inicializador

The user must have this script. Creates empty folder structure.  
El usuario debe tener este script. Crea la estructura de carpetas vacía.

### `init_py_app.ps1`

```powershell
# USAGE / USO: .\init_py_app.ps1 -Name "MyApp"
# If blocked / Si bloqueado: powershell -ExecutionPolicy Bypass -File init_py_app.ps1 -Name "MyApp"

param(
    [Parameter(Mandatory=$true)]
    [string]$Name,
    [string]$Path = (Get-Location).Path
)

$AppDir = Join-Path $Path $Name

# Folders / Carpetas
@(
    $AppDir,
    "$AppDir\src",
    "$AppDir\src\bin",
    "$AppDir\src\bin\modules",
    "$AppDir\dist"
) | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
        Write-Host "[OK] $_" -ForegroundColor Green
    }
}

# Placeholder files / Ficheros placeholder
@{
    "$AppDir\README.md" = "# $Name"
    "$AppDir\publish.bat" = "@echo off`nREM Ask Claude / Pedir a Claude"
    "$AppDir\src\1_Install.bat" = "@echo off`nREM Ask Claude / Pedir a Claude"
    "$AppDir\src\$Name.bat" = "@echo off`nREM Ask Claude / Pedir a Claude"
    "$AppDir\src\README.txt" = "$Name - Pending / Pendiente"
    "$AppDir\src\bin\main.py" = "# Ask Claude / Pedir a Claude"
    "$AppDir\src\bin\modules\__init__.py" = "# Modules package / Paquete de modulos"
    "$AppDir\src\bin\modules\config.py" = "# Ask Claude / Pedir a Claude"
    "$AppDir\src\bin\modules\app.py" = "# Ask Claude / Pedir a Claude"
}.GetEnumerator() | ForEach-Object {
    if (-not (Test-Path $_.Key)) {
        Set-Content -Path $_.Key -Value $_.Value -Encoding UTF8
        Write-Host "[OK] $($_.Key)" -ForegroundColor Green
    }
}

Write-Host "`n=== Structure created / Estructura creada: $Name ===" -ForegroundColor Cyan
Write-Host "Open chat with Claude and describe what you need" -ForegroundColor Gray
Write-Host "Abre chat con Claude y describe lo que necesitas" -ForegroundColor Gray
```

---

## Instructions for Claude (CRITICAL) / Instrucciones para Claude (CRÍTICO)

### The User Does NOT Know Python / El Usuario NO Sabe Python

They will describe their problem like this / Describirá su problema así:

> "I need to convert sales Excel files to PDF" / "Necesito convertir los Excel de ventas a PDF"  
> "I want to rename photos massively" / "Quiero renombrar fotos masivamente"  
> "I have to clean some messy CSVs" / "Tengo que limpiar unos CSV guarros"

### Default Assumptions / Asunciones por Defecto

- **ALWAYS GUI** (CustomTkinter) unless explicitly requesting script/console  
  **SIEMPRE GUI** (CustomTkinter) salvo que pida explícitamente script/consola
- **Window with button** to select files if working with files  
  **Ventana con botón** para seleccionar ficheros si trabaja con archivos
- **Dark theme / Tema oscuro**

### Conversation Flow / Flujo de Conversación

**1. Understand the problem (BUSINESS questions) / Entender el problema (preguntas de NEGOCIO):**

```
- What input files? (Excel, CSV, images...) / ¿Qué ficheros de entrada? (Excel, CSV, imágenes...)
- What result do you need? (PDF, clean file, rename...) / ¿Qué resultado necesitas? (PDF, fichero limpio, renombrar...)
- Any specific format or rules? / ¿Algún formato o regla específica?
```

**DO NOT ask / NO preguntar**: GUI/console, dependencies, architecture, classes...

**2. Propose name and start / Proponer nombre y arrancar:**

> "Perfect, we'll call it 'ExcelToPDF'.  
> Run this in PowerShell:  
> `.\init_py_app.ps1 -Name "ExcelToPDF"`  
> When done, tell me 'ready'."

> "Perfecto, la llamaremos 'ExcelToPDF'.  
> Ejecuta esto en PowerShell:  
> `.\init_py_app.ps1 -Name "ExcelToPDF"`  
> Cuando termine, dime 'listo'."

**3. Generate files ONE BY ONE / Generar ficheros UNO A UNO:**

Always indicate exact path and wait for confirmation:  
Siempre indicar ruta exacta y esperar confirmación:

> "Copy this and paste it in `src/bin/modules/config.py` (replace all content):"  
> "Copia esto y pégalo en `src/bin/modules/config.py` (reemplaza todo el contenido):"
> ```python
> [complete code / código completo]
> ```
> "Done? Tell me 'next'" / "¿Pegado? Dime 'siguiente'"

### Rules When Generating Code / Reglas al Generar Código

| Rule / Regla | Detail / Detalle |
|--------------|------------------|
| **COMPLETE CODE / CÓDIGO COMPLETO** | Never fragments, never "..." / Nunca fragmentos, nunca "..." |
| **NO PLACEHOLDERS** | Never `[AppName]`, use real name / Nunca `[NombreApp]`, usar nombre real |
| **COHERENT IMPORTS** | What app.py uses MUST be in config.py / Lo que use app.py DEBE estar en config.py |
| **~150 LINES MAX** | Fits in one copy/paste / Que quepa en un copy/paste |
| **EXACT PATH / RUTA EXACTA** | Always say where to paste / Siempre decir dónde pegar |
| **DEPENDENCIES / DEPENDENCIAS** | List in 1_Instalar.bat those needed by the app / Listar en 1_Instalar.bat las que necesite la app |

### File Order / Orden de Ficheros

```
1. config.py        → src/bin/modules/config.py
2. app.py           → src/bin/modules/app.py
3. (extra modules if needed / módulos extra si hacen falta)
4. main.py          → src/bin/main.py
5. 1_Install.bat    → src/1_Install.bat  (with specific dependencies / con dependencias específicas)
6. [Name].bat       → src/[Name].bat
7. README.txt       → src/README.txt
8. publish.bat      → publish.bat (ROOT, not in src / RAÍZ, no en src)
```

---

## Base Code - GUI App / Código Base - App GUI

### `config.py`

```python
# -*- coding: utf-8 -*-
"""
AppName - Global configuration / Configuración global

Author/Autor: [Your Name] ([your@email.com])
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: [Month Year] / [Mes Año]

Copyright (c) [Year] [Your Name]
Licensed under MIT License
"""

import os
import sys

# === APP INFO ===
APP_NAME = "AppName"
APP_VERSION = "1.0.0"

# === WINDOW / VENTANA ===
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

# === PATHS / RUTAS ===
def get_app_dir():
    """
    Get application root directory
    Obtiene directorio raíz de la aplicación
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

APP_DIR = get_app_dir()
```

### `app.py`

```python
# -*- coding: utf-8 -*-
"""
AppName - Main window / Ventana principal

Author/Autor: [Your Name] ([your@email.com])
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: [Month Year] / [Mes Año]

Copyright (c) [Year] [Your Name]
Licensed under MIT License
"""

import customtkinter as ctk
from .config import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT


class App(ctk.CTk):
    """Main application class / Clase principal de la aplicación"""
    
    def __init__(self):
        super().__init__()
        
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create UI widgets / Crea widgets de UI"""
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.label = ctk.CTkLabel(
            self.main_frame, 
            text="App working / App funcionando",
            font=("Arial", 18)
        )
        self.label.pack(pady=20)
        
        self.btn = ctk.CTkButton(
            self.main_frame,
            text="Select file / Seleccionar archivo",
            command=self._on_click
        )
        self.btn.pack(pady=10)
    
    def _on_click(self):
        """Handle button click / Maneja click en botón"""
        self.label.configure(text="Button pressed! / Boton pulsado!")
```

### `main.py`

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AppName - Entry point / Punto de entrada

Author/Autor: [Your Name] ([your@email.com])
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: [Month Year] / [Mes Año]

Copyright (c) [Year] [Your Name]
Licensed under MIT License
"""

from modules.app import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
```

---

## Base Code - Console App / Código Base - App Consola

For converters, data cleaners, batch scripts.  
Para converters, limpiadores de datos, scripts batch.

### `config.py` (console / consola)

```python
# -*- coding: utf-8 -*-
"""
AppName - Global configuration / Configuración global

Author/Autor: [Your Name] ([your@email.com])
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: [Month Year] / [Mes Año]

Copyright (c) [Year] [Your Name]
Licensed under MIT License
"""

import os
import sys

APP_NAME = "MyScript"
APP_VERSION = "1.0.0"

def get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

APP_DIR = get_app_dir()
```

### `app.py` (console / consola)

```python
# -*- coding: utf-8 -*-
"""
AppName - Main logic / Lógica principal

Author/Autor: [Your Name] ([your@email.com])
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: [Month Year] / [Mes Año]

Copyright (c) [Year] [Your Name]
Licensed under MIT License
"""

from .config import APP_NAME, APP_VERSION


class App:
    """Main application class / Clase principal de la aplicación"""
    
    def __init__(self):
        print(f"{APP_NAME} v{APP_VERSION}")
        print("=" * 40)
    
    def run(self):
        """Run main logic / Ejecuta lógica principal"""
        print("Running... / Ejecutando...")
        
        # Logic here / Lógica aquí
        
        print("")
        input("Press Enter to exit... / Pulsa Enter para salir...")
```

### `main.py` (console / consola)

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AppName - Entry point / Punto de entrada

Author/Autor: [Your Name] ([your@email.com])
Assistant/Asistente: Claude (Anthropic Opus 4.5)
Date/Fecha: [Month Year] / [Mes Año]

Copyright (c) [Year] [Your Name]
Licensed under MIT License
"""

from modules.app import App

if __name__ == "__main__":
    app = App()
    app.run()
```

---

## BAT Files / Archivos BAT

**IMPORTANT / IMPORTANTE**: Claude must replace `AppName` with the real name in ALL .bat files  
Claude debe reemplazar `NombreApp` por el nombre real en TODOS los .bat

### `1_Install.bat`

```batch
@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
title AppName - Installation

echo.
echo ============================================
echo       AppName - INSTALLATION
echo ============================================
echo.

REM Find Python / Buscar Python
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
    goto :found
)
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=py
    goto :found
)
if exist "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" (
    set "PYTHON_CMD=%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe"
    goto :found
)
echo ERROR: Python not found
echo Install Python from Microsoft Store
pause
exit /b 1

:found
echo Python: %PYTHON_CMD%
echo.
echo set PYTHON_CMD=%PYTHON_CMD%> "%~dp0_python_path.bat"

echo Installing dependencies...
"%PYTHON_CMD%" -m pip install --upgrade pip >nul 2>&1

REM === DEPENDENCIES (adapt per app) ===
"%PYTHON_CMD%" -m pip install customtkinter
REM "%PYTHON_CMD%" -m pip install openpyxl
REM "%PYTHON_CMD%" -m pip install pillow
REM "%PYTHON_CMD%" -m pip install pandas
REM === END DEPENDENCIES ===

if %ERRORLEVEL% NEQ 0 (
    echo ERROR installing
    pause
    exit /b 1
)

echo.
echo ============================================
echo         INSTALLATION COMPLETED
echo ============================================
echo You can now run: AppName.bat
pause
```

### `AppName.bat`

```batch
@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

if exist "%~dp0_python_path.bat" (
    call "%~dp0_python_path.bat"
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set PYTHON_CMD=python
    ) else (
        echo ERROR: Run 1_Install.bat first
        pause
        exit /b 1
    )
)

"%PYTHON_CMD%" "%~dp0bin\main.py"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error. Try running 1_Install.bat
    pause
)
```

### `README.txt`

```
============================================
         AppName v1.0.0
============================================

INSTALLATION (first time only)
------------------------------
1. Double-click: 1_Install.bat
2. Wait 1-2 minutes

USAGE
-----
Double-click: AppName.bat

TROUBLESHOOTING
---------------
- Python not found: Install from Microsoft Store
- Error: Run 1_Install.bat again
```

### `publish.bat`

```batch
@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

if not exist "src" (
    echo ERROR: src/ does not exist
    pause
    exit /b 1
)
if not exist "dist" mkdir dist

for /f "tokens=1-5 delims=/:. " %%a in ("%date% %time%") do (
    set "ZIPNAME=AppName_%%c%%b%%a_%%d%%e.zip"
)

set "TEMP_DIR=%TEMP%\AppName_pub"
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%\AppName"

copy "src\1_Install.bat" "%TEMP_DIR%\AppName\" >nul
copy "src\AppName.bat" "%TEMP_DIR%\AppName\" >nul
copy "src\README.txt" "%TEMP_DIR%\AppName\" >nul
xcopy /E /I /Q "src\bin" "%TEMP_DIR%\AppName\bin" >nul

powershell -NoProfile -Command "Compress-Archive -Path '%TEMP_DIR%\AppName' -DestinationPath 'dist\%ZIPNAME%' -Force"
rmdir /s /q "%TEMP_DIR%"

echo Published: dist\%ZIPNAME%
explorer "dist"
pause
```

---

## Final Structure / Estructura Final

```
AppName/
├── README.md
├── publish.bat
├── src/
│   ├── 1_Install.bat
│   ├── AppName.bat
│   ├── README.txt
│   └── bin/
│       ├── main.py
│       └── modules/
│           ├── __init__.py
│           ├── config.py
│           └── app.py
└── dist/
```

---

## Golden Rules / Reglas de Oro

1. **config.py FIRST** - Defines everything others use / Define todo lo que usan los demás
2. **NO PLACEHOLDERS** - Real names, real code / Nombres reales, código real
3. **COHERENT IMPORTS** - If app.py uses X, config.py defines it / Si app.py usa X, config.py lo define
4. **DEPENDENCIES IN 1_Instalar.bat** - Those needed by each app / Las que necesite cada app
5. **~150 LINES MAX** - One clean copy/paste / Un copy/paste limpio
6. **NO ACCENTS in .bat and LEEME.txt** - Pure ASCII / ASCII puro
