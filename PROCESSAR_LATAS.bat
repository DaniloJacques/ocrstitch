@echo off
title OCR de Latas - Processamento
color 0B

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                 🔍 PROCESSANDO LATAS 🔍                      ║
echo  ║                Leitura Automática OCR                        ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.

REM Verifica se existe pasta input_images
if not exist "input_images" (
    echo ❌ ERRO: Pasta "input_images" não encontrada!
    echo.
    echo 📁 SOLUÇÃO:
    echo    1. Crie a pasta "input_images" neste diretório
    echo    2. Coloque suas fotos de latas lá
    echo    3. Execute este script novamente
    echo.
    pause
    exit /b 1
)

REM Conta quantas imagens existem
set /a image_count=0
for %%f in (input_images\*.jpg input_images\*.jpeg input_images\*.png input_images\*.bmp input_images\*.tiff) do (
    set /a image_count+=1
)

if %image_count% EQU 0 (
    echo ⚠️  AVISO: Nenhuma imagem encontrada na pasta "input_images"
    echo.
    echo 📸 Formatos aceitos: JPG, PNG, BMP, TIFF
    echo.
    pause
    exit /b 1
)

echo 📸 Encontradas %image_count% imagens para processar
echo.
echo 🚀 Iniciando processamento OCR...
echo    Isso pode demorar alguns minutos dependendo da quantidade
echo.

REM Executa o processamento
python power_automate_integration.py input_images

if errorlevel 1 (
    echo.
    echo ❌ Erro durante o processamento!
    echo 📋 Verifique o arquivo de log na pasta "logs"
    echo.
    pause
    exit /b 1
)

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                    ✅ PROCESSAMENTO CONCLUÍDO!               ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🎉 Suas latas foram processadas com sucesso!
echo.
echo 📁 Resultados salvos em:
echo    📊 output_results\relatorio_ocr_latas_[DATA].xlsx
echo    📋 output_results\dados_ocr_latas_[DATA].csv
echo.
echo 💡 Dica: Abra o arquivo Excel para ver os resultados organizados!
echo.

REM Pergunta se quer abrir a pasta de resultados
set /p open_folder="Deseja abrir a pasta de resultados? (s/n): "
if /i "%open_folder%"=="s" (
    explorer output_results
)

echo.
echo 🔄 Para processar mais latas:
echo    1. Adicione novas fotos em "input_images"
echo    2. Execute este script novamente
echo.
pause
