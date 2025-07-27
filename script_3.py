# Criando o script de integração com Power Automate
power_automate_integration = '''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Power Automate Integration - Integração com Power Automate Desktop
Script para facilitar a integração entre o OCR local e Power Automate
Author: Confrade Tech Solutions
Date: 2025
"""

import os
import json
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import argparse

# Importa nossos módulos
try:
    from ocr_processor import OCRProcessor
    from excel_generator import ExcelGenerator
except ImportError as e:
    print(f"❌ Erro: Não foi possível importar módulos necessários: {e}")
    print("   Certifique-se de que todos os arquivos estão no mesmo diretório")
    sys.exit(1)

class PowerAutomateIntegration:
    """
    Classe para integração com Power Automate Desktop
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializa a integração
        
        Args:
            config_path: Caminho para arquivo de configuração (opcional)
        """
        self.config = self.load_config(config_path)
        self.setup_logging()
        
        # Inicializa processadores
        self.ocr_processor = OCRProcessor(
            tesseract_path=self.config.get('tesseract_path')
        )
        self.excel_generator = ExcelGenerator()
        
        logger.info("Power Automate Integration inicializada")
    
    def load_config(self, config_path: Optional[str]) -> Dict:
        """
        Carrega configurações do arquivo JSON
        
        Args:
            config_path: Caminho para o arquivo de configuração
            
        Returns:
            Dicionário com configurações
        """
        if not config_path:
            config_path = Path('config') / 'settings.json'
        
        try:
            if Path(config_path).exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                print(f"✅ Configuração carregada: {config_path}")
                return config
            else:
                print(f"⚠️  Arquivo de configuração não encontrado: {config_path}")
                return self.get_default_config()
        
        except Exception as e:
            print(f"❌ Erro ao carregar configuração: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """
        Retorna configuração padrão
        
        Returns:
            Dicionário com configurações padrão
        """
        return {
            "tesseract_path": "",
            "input_folder": "input_images",
            "output_folder": "output_results",
            "log_level": "INFO",
            "supported_formats": [".jpg", ".jpeg", ".png", ".bmp", ".tiff"],
            "ocr_config": "--oem 3 --psm 8",
            "business_rules": {
                "SP": "Produto de São Paulo",
                "RJ": "Produto do Rio de Janeiro",
                "BR": "Produto Nacional"
            }
        }
    
    def setup_logging(self):
        """
        Configura sistema de logging
        """
        log_level = getattr(logging, self.config.get('log_level', 'INFO'))
        
        # Cria pasta de logs se não existir
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # Configura logging
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'power_automate_integration.log'),
                logging.StreamHandler()
            ]
        )
        
        global logger
        logger = logging.getLogger(__name__)
    
    def process_workflow(self, input_path: str, generate_excel: bool = True, generate_csv: bool = True) -> Dict:
        """
        Executa o workflow completo de OCR e geração de relatórios
        
        Args:
            input_path: Caminho para imagem ou pasta com imagens
            generate_excel: Se deve gerar arquivo Excel
            generate_csv: Se deve gerar arquivo CSV
            
        Returns:
            Dicionário com informações sobre os arquivos gerados
        """
        try:
            logger.info(f"Iniciando workflow para: {input_path}")
            
            # Validação do caminho de entrada
            input_path = Path(input_path)
            if not input_path.exists():
                raise FileNotFoundError(f"Caminho não encontrado: {input_path}")
            
            # Processamento OCR
            if input_path.is_file():
                results = [self.ocr_processor.process_single_image(str(input_path))]
            elif input_path.is_dir():
                results = self.ocr_processor.process_folder(str(input_path))
            else:
                raise ValueError(f"Caminho inválido: {input_path}")
            
            # Salva resultados JSON temporário
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_path = Path(self.config['output_folder']) / f"ocr_results_{timestamp}.json"
            
            # Garante que pasta de saída existe
            json_path.parent.mkdir(exist_ok=True)
            
            self.ocr_processor.save_results_json(results, str(json_path))
            
            generated_files = {
                'json_file': str(json_path),
                'excel_file': None,
                'csv_file': None,
                'timestamp': timestamp,
                'total_images': len(results),
                'successful': len([r for r in results if r['status'] == 'sucesso']),
                'errors': len([r for r in results if r['status'] == 'erro'])
            }
            
            # Gera Excel se solicitado
            if generate_excel:
                excel_path = self.excel_generator.generate_excel(str(json_path))
                generated_files['excel_file'] = excel_path
                logger.info(f"Excel gerado: {excel_path}")
            
            # Gera CSV se solicitado
            if generate_csv:
                csv_path = self.excel_generator.generate_csv_for_power_automate(str(json_path))
                generated_files['csv_file'] = csv_path
                logger.info(f"CSV gerado: {csv_path}")
            
            logger.info("Workflow concluído com sucesso")
            return generated_files
            
        except Exception as e:
            logger.error(f"Erro no workflow: {str(e)}")
            raise
    
    def create_power_automate_response(self, workflow_result: Dict) -> Dict:
        """
        Cria resposta formatada para o Power Automate
        
        Args:
            workflow_result: Resultado do workflow
            
        Returns:
            Resposta formatada para Power Automate
        """
        return {
            "success": True,
            "message": "Processamento OCR concluído com sucesso",
            "data": {
                "timestamp": workflow_result['timestamp'],
                "total_images": workflow_result['total_images'],
                "successful_ocr": workflow_result['successful'],
                "failed_ocr": workflow_result['errors'],
                "success_rate": round((workflow_result['successful'] / max(workflow_result['total_images'], 1)) * 100, 2),
                "files_generated": {
                    "json_results": workflow_result['json_file'],
                    "excel_report": workflow_result['excel_file'],
                    "csv_data": workflow_result['csv_file']
                }
            }
        }
    
    def run_for_power_automate(self, input_folder: str) -> str:
        """
        Executa processamento otimizado para Power Automate
        
        Args:
            input_folder: Pasta com imagens para processar
            
        Returns:
            JSON string com resultado formatado
        """
        try:
            # Executa workflow
            result = self.process_workflow(input_folder, generate_excel=True, generate_csv=True)
            
            # Formata resposta
            response = self.create_power_automate_response(result)
            
            # Salva resposta para Power Automate
            timestamp = result['timestamp']
            response_path = Path(self.config['output_folder']) / f"power_automate_response_{timestamp}.json"
            
            with open(response_path, 'w', encoding='utf-8') as f:
                json.dump(response, f, ensure_ascii=False, indent=2)
            
            # Retorna JSON como string para Power Automate
            return json.dumps(response, ensure_ascii=False)
            
        except Exception as e:
            error_response = {
                "success": False,
                "message": f"Erro no processamento: {str(e)}",
                "data": None
            }
            return json.dumps(error_response, ensure_ascii=False)
    
    def monitor_folder(self, watch_folder: str, output_folder: Optional[str] = None):
        """
        Monitora pasta para processamento automático (para uso futuro)
        
        Args:
            watch_folder: Pasta para monitorar
            output_folder: Pasta de saída (opcional)
        """
        # Implementação futura para monitoramento automático
        logger.info(f"Monitoramento de pasta não implementado ainda: {watch_folder}")
        pass


def main():
    """
    Função principal para execução via linha de comando
    """
    parser = argparse.ArgumentParser(
        description='Integração OCR com Power Automate Desktop'
    )
    
    parser.add_argument(
        'input_path',
        help='Caminho para imagem ou pasta com imagens'
    )
    
    parser.add_argument(
        '--config',
        help='Caminho para arquivo de configuração'
    )
    
    parser.add_argument(
        '--excel-only',
        action='store_true',
        help='Gera apenas arquivo Excel'
    )
    
    parser.add_argument(
        '--csv-only',
        action='store_true',
        help='Gera apenas arquivo CSV'
    )
    
    parser.add_argument(
        '--power-automate',
        action='store_true',
        help='Modo Power Automate (retorna JSON)'
    )
    
    args = parser.parse_args()
    
    try:
        # Inicializa integração
        integration = PowerAutomateIntegration(config_path=args.config)
        
        if args.power_automate:
            # Modo Power Automate
            response = integration.run_for_power_automate(args.input_path)
            print(response)
        
        else:
            # Modo normal
            generate_excel = not args.csv_only
            generate_csv = not args.excel_only
            
            result = integration.process_workflow(
                args.input_path,
                generate_excel=generate_excel,
                generate_csv=generate_csv
            )
            
            print("\\n🎉 PROCESSAMENTO CONCLUÍDO!")
            print("=" * 40)
            print(f"📊 Total de imagens: {result['total_images']}")
            print(f"✅ Sucessos: {result['successful']}")
            print(f"❌ Erros: {result['errors']}")
            print(f"📈 Taxa de sucesso: {(result['successful'] / max(result['total_images'], 1) * 100):.1f}%")
            print("\\n📁 Arquivos gerados:")
            print(f"   📄 JSON: {result['json_file']}")
            if result['excel_file']:
                print(f"   📊 Excel: {result['excel_file']}")
            if result['csv_file']:
                print(f"   📋 CSV: {result['csv_file']}")
    
    except Exception as e:
        if args.power_automate:
            error_response = {
                "success": False,
                "message": f"Erro: {str(e)}",
                "data": None
            }
            print(json.dumps(error_response, ensure_ascii=False))
        else:
            print(f"❌ Erro: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
'''

# Salva o arquivo de integração
with open('power_automate_integration.py', 'w', encoding='utf-8') as f:
    f.write(power_automate_integration)

print("✅ Arquivo 'power_automate_integration.py' criado com sucesso!")
print("🤖 Script de integração Power Automate criado com:")
print("   - Workflow completo (OCR + Excel + CSV)")
print("   - Resposta formatada para Power Automate")
print("   - Sistema de configuração flexível")
print("   - Logging detalhado")
print("   - Tratamento de erros robusto")