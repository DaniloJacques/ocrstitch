@echo off
title Instalação OCR de Latas
color 0A

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                    OCR DE LATAS - SETUP                     ║
echo  ║                   100%% GRATUITO E OFFLINE                   ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🚀 Instalando sistema OCR para leitura automática de latas...
echo ⏱️  Isso pode demorar alguns minutos na primeira vez
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não encontrado!
    echo.
    echo 📥 SOLUÇÃO:
    echo    1. Acesse: https://www.python.org/downloads/
    echo    2. Baixe e instale o Python
    echo    3. IMPORTANTE: Marque "Add Python to PATH"
    echo    4. Execute este instalador novamente
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado!
echo.
echo 📦 Instalando bibliotecas necessárias...
echo    (opencv, tesseract, pandas, openpyxl...)
echo.

REM Instala dependências Python
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ Erro na instalação das bibliotecas Python
    echo 💡 Tente executar como Administrador
    pause
    exit /b 1
)

echo.
echo ✅ Bibliotecas Python instaladas!
echo.
echo 🔧 Configurando ambiente...

REM Executa setup do projeto
python setup.py

if errorlevel 1 (
    echo.
    echo ❌ Erro na configuração do projeto
    pause
    exit /b 1
)

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                     ✅ INSTALAÇÃO CONCLUÍDA!                 ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🎉 Sistema OCR instalado com sucesso!
echo.
echo 📁 Como usar:
echo    1. Coloque fotos das latas na pasta "input_images"
echo    2. Execute "PROCESSAR_LATAS.bat"
echo    3. Pegue sua planilha na pasta "output_results"
echo.
echo 💡 ATENÇÃO: Se houver erro com Tesseract, baixe em:
echo    https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo 📖 Leia o arquivo README.md para instruções detalhadas
echo.
pause
