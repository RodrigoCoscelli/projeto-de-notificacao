@echo off
echo ==========================================
echo    Iniciando o Notifica AME PG (Backend)
echo ==========================================
echo.

REM --- Verifica se o venv existe ---
if not exist venv\Scripts\activate.bat (
    echo [AVISO] Ambiente virtual nao encontrado. Criando venv...
    python -m venv venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar o ambiente virtual. Verifique se o Python esta instalado.
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtual criado.
)

REM --- Verifica se as dependencias estao instaladas ---
venv\Scripts\python.exe -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [AVISO] Dependencias nao encontradas. Instalando agora...
    venv\Scripts\pip.exe install -r requirements.txt
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependencias. Verifique sua conexao com a internet.
        pause
        exit /b 1
    )
    echo [OK] Dependencias instaladas com sucesso!
    echo.
)

echo Iniciando o Uvicorn...
venv\Scripts\uvicorn.exe backend.main:app --reload

pause
