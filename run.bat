@echo off
echo ==========================================
echo    Iniciando o Notifica AME PG (Backend)
echo ==========================================
echo.

if not exist venv\Scripts\activate.bat goto no_venv
call venv\Scripts\activate.bat
goto start_server

:no_venv
echo [AVISO] Ambiente virtual (venv) nao encontrado. O servidor tentara rodar globalmente.

:start_server
echo Iniciando o Uvicorn...
uvicorn backend.main:app --reload

pause
