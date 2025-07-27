#!/bin/bash

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

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
image_count=$(find input_images -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.bmp" -o -iname "*.tiff" \) | wc -l)

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
