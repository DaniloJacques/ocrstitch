# Vou criar a estrutura completa do projeto OCR offline
# Começando com o módulo principal de OCR

# Criando o arquivo principal ocr_processor.py
ocr_main_code = '''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR Processor Local - Extração de texto de imagens de latas
Sistema de processamento OCR offline usando Tesseract
Author: Confrade Tech Solutions
Date: 2025
"""

import os
import cv2
import json
import logging
import pytesseract
import numpy as np
from PIL import Image, ImageEnhance
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import re
from datetime import datetime

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ocr_processor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OCRProcessor:
    """
    Classe principal para processamento OCR de imagens de latas
    """
    
    def __init__(self, tesseract_path: Optional[str] = None):
        """
        Inicializa o processador OCR
        
        Args:
            tesseract_path: Caminho para o executável do Tesseract (opcional)
        """
        # Configuração do caminho do Tesseract (Windows)
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        elif os.name == 'nt':  # Windows
            pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        
        # Configurações do OCR
        self.ocr_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-_'
        
        # Extensões de imagem suportadas
        self.supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
        
        # Regras de negócio para observações
        self.business_rules = {
            'SP': 'Produto de São Paulo',
            'RJ': 'Produto do Rio de Janeiro',
            'MG': 'Produto de Minas Gerais',
            'BR': 'Produto Nacional',
            'EXP': 'Produto para Exportação',
            'IMP': 'Produto Importado'
        }
        
        logger.info("OCR Processor iniciado com sucesso")
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Pré-processa a imagem para melhorar a precisão do OCR
        
        Args:
            image_path: Caminho para a imagem
            
        Returns:
            Imagem pré-processada como array numpy
        """
        try:
            # Carrega a imagem
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Não foi possível carregar a imagem: {image_path}")
            
            # Converte para RGB (OpenCV usa BGR por padrão)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Redimensiona a imagem se for muito pequena (melhora OCR)
            height, width = image_rgb.shape[:2]
            if width < 300 or height < 200:
                scale_factor = max(300/width, 200/height)
                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)
                image_rgb = cv2.resize(image_rgb, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
            
            # Converte para escala de cinza
            gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
            
            # Aplicar filtro bilateral para reduzir ruído mantendo as bordas
            gray = cv2.bilateralFilter(gray, 11, 17, 17)
            
            # Threshold adaptativo para binarização
            binary = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Operações morfológicas para limpar a imagem
            kernel = np.ones((2, 2), np.uint8)
            processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            processed = cv2.morphologyEx(processed, cv2.MORPH_OPEN, kernel)
            
            # Inversão se necessário (Tesseract espera texto preto em fundo branco)
            if np.mean(processed) > 127:
                processed = cv2.bitwise_not(processed)
            
            logger.debug(f"Pré-processamento concluído para: {image_path}")
            return processed
            
        except Exception as e:
            logger.error(f"Erro no pré-processamento da imagem {image_path}: {str(e)}")
            raise
    
    def extract_text(self, processed_image: np.ndarray) -> str:
        """
        Extrai texto da imagem pré-processada usando Tesseract
        
        Args:
            processed_image: Imagem pré-processada
            
        Returns:
            Texto extraído
        """
        try:
            # Converte numpy array para PIL Image
            pil_image = Image.fromarray(processed_image)
            
            # Extrai texto usando Tesseract
            text = pytesseract.image_to_string(pil_image, config=self.ocr_config)
            
            # Limpa o texto extraído
            text = text.strip().replace('\\n', ' ').replace('\\t', ' ')
            text = re.sub(r'\\s+', ' ', text)  # Remove espaços múltiplos
            
            logger.debug(f"Texto extraído: {text}")
            return text
            
        except Exception as e:
            logger.error(f"Erro na extração de texto: {str(e)}")
            return ""
    
    def apply_business_rules(self, text: str) -> Tuple[str, str]:
        """
        Aplica regras de negócio ao texto extraído
        
        Args:
            text: Texto extraído do OCR
            
        Returns:
            Tupla com (texto_limpo, observação)
        """
        observation = ""
        
        # Procura por padrões nas regras de negócio
        for code, rule in self.business_rules.items():
            if code in text.upper():
                observation += f"{rule}; "
        
        # Remove ponto e vírgula final
        observation = observation.rstrip('; ')
        
        # Se não encontrou nenhuma regra, adiciona observação padrão
        if not observation:
            observation = "Verificar manualmente"
        
        return text, observation
    
    def process_single_image(self, image_path: str) -> Dict:
        """
        Processa uma única imagem
        
        Args:
            image_path: Caminho para a imagem
            
        Returns:
            Dicionário com os resultados do processamento
        """
        try:
            logger.info(f"Processando imagem: {image_path}")
            
            # Pré-processamento
            processed_image = self.preprocess_image(image_path)
            
            # Extração de texto
            raw_text = self.extract_text(processed_image)
            
            # Aplicação das regras de negócio
            clean_text, observation = self.apply_business_rules(raw_text)
            
            # Preparar resultado
            result = {
                'arquivo': os.path.basename(image_path),
                'caminho_completo': image_path,
                'texto_extraido': raw_text,
                'texto_limpo': clean_text,
                'observacao': observation,
                'timestamp': datetime.now().isoformat(),
                'status': 'sucesso'
            }
            
            logger.info(f"Processamento concluído: {image_path}")
            return result
            
        except Exception as e:
            logger.error(f"Erro no processamento da imagem {image_path}: {str(e)}")
            return {
                'arquivo': os.path.basename(image_path),
                'caminho_completo': image_path,
                'texto_extraido': '',
                'texto_limpo': '',
                'observacao': f'ERRO: {str(e)}',
                'timestamp': datetime.now().isoformat(),
                'status': 'erro'
            }
    
    def process_folder(self, folder_path: str) -> List[Dict]:
        """
        Processa todas as imagens em uma pasta
        
        Args:
            folder_path: Caminho para a pasta com imagens
            
        Returns:
            Lista com resultados de todas as imagens processadas
        """
        folder_path = Path(folder_path)
        if not folder_path.exists():
            raise ValueError(f"Pasta não encontrada: {folder_path}")
        
        results = []
        image_files = []
        
        # Encontra todos os arquivos de imagem
        for ext in self.supported_extensions:
            image_files.extend(folder_path.glob(f"*{ext}"))
            image_files.extend(folder_path.glob(f"*{ext.upper()}"))
        
        if not image_files:
            logger.warning(f"Nenhuma imagem encontrada em: {folder_path}")
            return results
        
        logger.info(f"Encontradas {len(image_files)} imagens para processar")
        
        # Processa cada imagem
        for i, image_file in enumerate(image_files, 1):
            logger.info(f"Processando {i}/{len(image_files)}: {image_file.name}")
            result = self.process_single_image(str(image_file))
            results.append(result)
        
        return results
    
    def save_results_json(self, results: List[Dict], output_path: str):
        """
        Salva os resultados em formato JSON
        
        Args:
            results: Lista com resultados do processamento
            output_path: Caminho para salvar o arquivo JSON
        """
        try:
            output_data = {
                'timestamp': datetime.now().isoformat(),
                'total_processadas': len(results),
                'sucessos': len([r for r in results if r['status'] == 'sucesso']),
                'erros': len([r for r in results if r['status'] == 'erro']),
                'resultados': results
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Resultados salvos em: {output_path}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar resultados JSON: {str(e)}")
            raise


def main():
    """
    Função principal para execução standalone
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='OCR Processor para imagens de latas')
    parser.add_argument('input_path', help='Caminho para imagem ou pasta com imagens')
    parser.add_argument('-o', '--output', help='Caminho para arquivo de saída JSON')
    parser.add_argument('-t', '--tesseract', help='Caminho para executável do Tesseract')
    
    args = parser.parse_args()
    
    # Inicializa o processador
    processor = OCRProcessor(tesseract_path=args.tesseract)
    
    # Determina se é arquivo ou pasta
    input_path = Path(args.input_path)
    
    if input_path.is_file():
        results = [processor.process_single_image(str(input_path))]
    elif input_path.is_dir():
        results = processor.process_folder(str(input_path))
    else:
        print(f"Erro: Caminho não encontrado: {input_path}")
        return
    
    # Define caminho de saída
    if args.output:
        output_path = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"ocr_results_{timestamp}.json"
    
    # Salva resultados
    processor.save_results_json(results, output_path)
    
    # Exibe resumo
    sucessos = len([r for r in results if r['status'] == 'sucesso'])
    erros = len([r for r in results if r['status'] == 'erro'])
    
    print(f"\\n=== RESUMO DO PROCESSAMENTO ===")
    print(f"Total de imagens: {len(results)}")
    print(f"Sucessos: {sucessos}")
    print(f"Erros: {erros}")
    print(f"Resultados salvos em: {output_path}")


if __name__ == "__main__":
    main()
'''

# Salva o código em um arquivo
with open('ocr_processor.py', 'w', encoding='utf-8') as f:
    f.write(ocr_main_code)

print("✅ Arquivo 'ocr_processor.py' criado com sucesso!")
print("📋 Módulo principal de OCR criado com:")
print("   - Pré-processamento avançado de imagens")
print("   - Extração de texto com Tesseract")
print("   - Aplicação de regras de negócio")
print("   - Processamento em lote")
print("   - Sistema de logging")