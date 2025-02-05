@ECHO OFF
SET ThisScriptsDirectory=%~dp0
SET PowerShellScriptPath="%ThisScriptsDirectory%Ollama-Run.ps1"
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File ""%PowerShellScriptPath%""' -Verb RunAs}";