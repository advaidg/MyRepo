@echo off
set "zipPath=C:\Path\To\7zip\7z.exe"
set "rootFolder=C:\Path\To\Your\Folders"

cd /d "%rootFolder%"

for /r %%i in (*) do (
    "%zipPath%" x "%%i" -o"%%~dpi"
)
