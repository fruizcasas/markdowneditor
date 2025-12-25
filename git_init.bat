@echo off
cd /d "%~dp0"

echo ============================================================
echo   Markdown Editor - Git Init and Push
echo ============================================================
echo.

echo Initializing git repository...
git init

echo Adding remote...
git remote add origin https://git.aurinkapv.com/python/markdowneditor.git

echo Adding files...
git add .

echo Creating initial commit...
git commit -m "Initial commit: Markdown Editor v1.2.0

Features:
- Live preview editor with split view
- Multi-language UI (EN/ES/FR/DE/IT/PT/ZH)
- CSS style profiles with visual editor
- PDF export (wkhtmltopdf)
- HTML export for Outlook
- Find and Replace (Ctrl+F / Ctrl+H)
- Drag and drop .md files
- Dark/Light theme toggle
- Freeze preview for large files
- Editor and preview zoom controls
- Bilingual code comments (EN/ES)

Co-authored-by: Claude (Anthropic Opus 4.5)"

echo Pushing to remote...
git branch -M main
git push -u origin main

echo.
echo ============================================================
echo   Done! Repository pushed to:
echo   https://git.aurinkapv.com/python/markdowneditor.git
echo ============================================================
pause
