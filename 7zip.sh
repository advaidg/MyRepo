@echo off
set "zipPath=C:\Path\To\7zip\7z.exe"
set "rootFolder=C:\Path\To\Your\Folders"

cd /d "%rootFolder%"

for /r %%i in (*) do (
    if "%%~xi"==".zip" (
        set "outputFolder=%%~ni"
        md "!outputFolder!" 2>nul
        "%zipPath%" x "%%i" -o"!outputFolder!"
    )
)
