# Criando requirements.txt
requirements_content = '''# OCR de Latas - Dependências Python
# Todas as bibliotecas são 100% GRATUITAS!

# Processamento de imagens
opencv-python>=4.5.0

# OCR (Reconhecimento de texto)
pytesseract>=0.3.8

# Manipulação de imagens
Pillow>=8.0.0

# Computação científica
numpy>=1.19.0

# Manipulação de dados
pandas>=1.3.0

# Manipulação de Excel
openpyxl>=3.0.7

# Requisições HTTP (para possíveis expansões futuras)
requests>=2.25.0
'''

with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write(requirements_content)

print("✅ requirements.txt criado!")

# Criando scripts de instalação automática ultra-simples
install_bat = '''@echo off
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
'''

with open('INSTALAR.bat', 'w', encoding='utf-8') as f:
    f.write(install_bat)

print("✅ INSTALAR.bat criado para Windows!")

# Script de instalação para Linux/Mac
install_sh = '''#!/bin/bash

# Cores para output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
BLUE='\\033[0;34m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    OCR DE LATAS - SETUP                     ║"
echo "║                   100% GRATUITO E OFFLINE                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Instalando sistema OCR para leitura automática de latas..."
echo "⏱️  Isso pode demorar alguns minutos na primeira vez"
echo ""

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verifica Python3
if ! command_exists python3; then
    echo -e "${RED}❌ ERRO: Python 3 não encontrado!${NC}"
    echo ""
    echo "📥 SOLUÇÃO:"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "   Mac: brew install python3"
        echo "   Ou baixe em: https://www.python.org/downloads/"
    elif [[ "$OSTYPE" == "linux"* ]]; then
        echo "   Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"
        echo "   CentOS/RHEL: sudo yum install python3 python3-pip"
    fi
    
    echo ""
    read -p "Pressione Enter para sair..."
    exit 1
fi

echo "✅ Python 3 encontrado!"

# Verifica pip
if ! command_exists pip3; then
    echo "📦 Instalando pip..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py
        rm get-pip.py
    elif [[ "$OSTYPE" == "linux"* ]]; then
        sudo apt update
        sudo apt install -y python3-pip
    fi
fi

echo ""
echo "📦 Instalando bibliotecas necessárias..."
echo "   (opencv, tesseract, pandas, openpyxl...)"
echo ""

# Instala dependências Python
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Erro na instalação das bibliotecas Python${NC}"
    echo "💡 Tente com: sudo python3 -m pip install -r requirements.txt"
    read -p "Pressione Enter para sair..."
    exit 1
fi

echo ""
echo "✅ Bibliotecas Python instaladas!"
echo ""
echo "🔧 Configurando ambiente..."

# Executa setup do projeto
python3 setup.py

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Erro na configuração do projeto${NC}"
    read -p "Pressione Enter para sair..."
    exit 1
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                     ✅ INSTALAÇÃO CONCLUÍDA!                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🎉 Sistema OCR instalado com sucesso!"
echo ""
echo "📁 Como usar:"
echo "   1. Coloque fotos das latas na pasta 'input_images'"
echo "   2. Execute './PROCESSAR_LATAS.sh'"
echo "   3. Pegue sua planilha na pasta 'output_results'"
echo ""

# Verifica Tesseract
if ! command_exists tesseract; then
    echo -e "${YELLOW}💡 ATENÇÃO: Tesseract OCR não encontrado${NC}"
    echo "   Instale com:"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "   brew install tesseract"
    elif [[ "$OSTYPE" == "linux"* ]]; then
        echo "   sudo apt install tesseract-ocr"
    fi
    echo ""
fi

echo "📖 Leia o arquivo README.md para instruções detalhadas"
echo ""
read -p "Pressione Enter para continuar..."
'''

with open('INSTALAR.sh', 'w', encoding='utf-8') as f:
    f.write(install_sh)

# Torna o script executável
import os
os.chmod('INSTALAR.sh', 0o755)

print("✅ INSTALAR.sh criado para Linux/Mac!")

# Scripts de execução ultra-simples
processar_bat = '''@echo off
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
for %%f in (input_images\\*.jpg input_images\\*.jpeg input_images\\*.png input_images\\*.bmp input_images\\*.tiff) do (
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
echo    📊 output_results\\relatorio_ocr_latas_[DATA].xlsx
echo    📋 output_results\\dados_ocr_latas_[DATA].csv
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
'''

with open('PROCESSAR_LATAS.bat', 'w', encoding='utf-8') as f:
    f.write(processar_bat)

print("✅ PROCESSAR_LATAS.bat criado!")

# Script de processamento para Linux/Mac
processar_sh = '''#!/bin/bash

# Cores
RED='\\033[0;31m'
GREEN='\\033[0;32m'
BLUE='\\033[0;34m'
YELLOW='\\033[1;33m'
NC='\\033[0m'

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                 🔍 PROCESSANDO LATAS 🔍                      ║"
echo "║                Leitura Automática OCR                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Verifica se existe pasta input_images
if [ ! -d "input_images" ]; then
    echo -e "${RED}❌ ERRO: Pasta 'input_images' não encontrada!${NC}"
    echo ""
    echo "📁 SOLUÇÃO:"
    echo "   1. Crie a pasta 'input_images' neste diretório"
    echo "   2. Coloque suas fotos de latas lá"
    echo "   3. Execute este script novamente"
    echo ""
    read -p "Pressione Enter para sair..."
    exit 1
fi

# Conta quantas imagens existem
image_count=$(find input_images -type f \\( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.bmp" -o -iname "*.tiff" \\) | wc -l)

if [ $image_count -eq 0 ]; then
    echo -e "${YELLOW}⚠️  AVISO: Nenhuma imagem encontrada na pasta 'input_images'${NC}"
    echo ""
    echo "📸 Formatos aceitos: JPG, PNG, BMP, TIFF"
    echo ""
    read -p "Pressione Enter para sair..."
    exit 1
fi

echo "📸 Encontradas $image_count imagens para processar"
echo ""
echo "🚀 Iniciando processamento OCR..."
echo "   Isso pode demorar alguns minutos dependendo da quantidade"
echo ""

# Executa o processamento
python3 power_automate_integration.py input_images

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Erro durante o processamento!${NC}"
    echo "📋 Verifique o arquivo de log na pasta 'logs'"
    echo ""
    read -p "Pressione Enter para sair..."
    exit 1
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    ✅ PROCESSAMENTO CONCLUÍDO!               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🎉 Suas latas foram processadas com sucesso!"
echo ""
echo "📁 Resultados salvos em:"
echo "   📊 output_results/relatorio_ocr_latas_[DATA].xlsx"
echo "   📋 output_results/dados_ocr_latas_[DATA].csv"
echo ""
echo "💡 Dica: Abra o arquivo Excel para ver os resultados organizados!"
echo ""

# Pergunta se quer abrir a pasta de resultados
read -p "Deseja abrir a pasta de resultados? (s/n): " open_folder
if [[ "$open_folder" == "s" || "$open_folder" == "S" ]]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open output_results
    elif [[ "$OSTYPE" == "linux"* ]]; then
        xdg-open output_results 2>/dev/null || nautilus output_results 2>/dev/null || echo "Abra manualmente a pasta: output_results"
    fi
fi

echo ""
echo "🔄 Para processar mais latas:"
echo "   1. Adicione novas fotos em 'input_images'"
echo "   2. Execute este script novamente"
echo ""
read -p "Pressione Enter para continuar..."
'''

with open('PROCESSAR_LATAS.sh', 'w', encoding='utf-8') as f:
    f.write(processar_sh)

# Torna executável
os.chmod('PROCESSAR_LATAS.sh', 0o755)

print("✅ PROCESSAR_LATAS.sh criado!")
print("\n🎉 PROJETO COMPLETO CRIADO!")
print("=" * 50)
print("📁 Arquivos gerados:")
print("   🐍 ocr_processor.py            (OCR principal)")
print("   📊 excel_generator.py          (Gerador Excel)")
print("   🔧 setup.py                    (Configurador)")
print("   🤖 power_automate_integration.py (Integração)")
print("   📖 README.md                   (Manual)")
print("   📦 requirements.txt            (Dependências)")
print("   🚀 INSTALAR.bat/.sh            (Instalador)")
print("   ▶️  PROCESSAR_LATAS.bat/.sh     (Executor)")
print("\n💡 PARA O SEU AMIGO:")
print("   1. Baixar todos os arquivos")
print("   2. Executar INSTALAR")
print("   3. Colocar fotos em input_images")
print("   4. Executar PROCESSAR_LATAS")
print("   5. Pegar Excel na pasta output_results")
print("\n💰 CUSTO TOTAL: R$ 0,00 (100% gratuito!)")