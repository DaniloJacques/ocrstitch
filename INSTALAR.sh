#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

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
