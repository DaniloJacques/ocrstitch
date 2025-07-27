# Criando o script de instalação e configuração
setup_script = '''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup Script - Configuração do ambiente OCR
Script para instalação e configuração do projeto OCR Local
Author: Confrade Tech Solutions
Date: 2025
"""

import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
import shutil
from pathlib import Path
import json

class OCRSetup:
    """
    Classe para configuração do ambiente OCR
    """
    
    def __init__(self):
        self.system = platform.system()
        self.python_version = sys.version_info
        self.project_dir = Path.cwd()
        
        print("🚀 Iniciando configuração do ambiente OCR Local")
        print(f"   Sistema: {self.system}")
        print(f"   Python: {self.python_version.major}.{self.python_version.minor}")
        print(f"   Diretório: {self.project_dir}")
        print("-" * 50)
    
    def check_python_version(self):
        """Verifica se a versão do Python é compatível"""
        print("🔍 Verificando versão do Python...")
        
        if self.python_version.major < 3 or (self.python_version.major == 3 and self.python_version.minor < 7):
            print("❌ Erro: Python 3.7+ é necessário")
            print("   Por favor, atualize sua versão do Python")
            return False
        
        print(f"✅ Python {self.python_version.major}.{self.python_version.minor} é compatível")
        return True
    
    def install_python_packages(self):
        """Instala os pacotes Python necessários"""
        print("📦 Instalando pacotes Python...")
        
        packages = [
            'opencv-python>=4.5.0',
            'pytesseract>=0.3.8',
            'pillow>=8.0.0',
            'numpy>=1.19.0',
            'pandas>=1.3.0',
            'openpyxl>=3.0.7',
            'requests>=2.25.0'
        ]
        
        for package in packages:
            try:
                print(f"   Instalando {package}...")
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', package, '--upgrade'
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"   ✅ {package} instalado")
            except subprocess.CalledProcessError:
                print(f"   ❌ Erro ao instalar {package}")
                return False
        
        print("✅ Todos os pacotes Python foram instalados")
        return True
    
    def install_tesseract_windows(self):
        """Instala Tesseract no Windows"""
        print("🔧 Configurando Tesseract para Windows...")
        
        tesseract_paths = [
            r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
            r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe",
            r"C:\\tesseract\\tesseract.exe"
        ]
        
        # Verifica se já está instalado
        for path in tesseract_paths:
            if os.path.exists(path):
                print(f"✅ Tesseract encontrado em: {path}")
                return path
        
        print("⚠️  Tesseract não encontrado no sistema")
        print("📥 Instruções para instalação:")
        print("   1. Baixe o Tesseract do link:")
        print("      https://github.com/UB-Mannheim/tesseract/wiki")
        print("   2. Execute o instalador como administrador")
        print("   3. Certifique-se de marcar 'Add to PATH' durante a instalação")
        print("   4. Execute este script novamente após a instalação")
        
        return None
    
    def install_tesseract_linux(self):
        """Instala Tesseract no Linux"""
        print("🔧 Configurando Tesseract para Linux...")
        
        # Verifica se já está instalado
        try:
            result = subprocess.run(['which', 'tesseract'], capture_output=True, text=True)
            if result.returncode == 0:
                tesseract_path = result.stdout.strip()
                print(f"✅ Tesseract encontrado em: {tesseract_path}")
                return tesseract_path
        except:
            pass
        
        print("📦 Instalando Tesseract...")
        
        try:
            # Ubuntu/Debian
            subprocess.check_call(['sudo', 'apt', 'update'], stdout=subprocess.DEVNULL)
            subprocess.check_call(['sudo', 'apt', 'install', '-y', 'tesseract-ocr'], stdout=subprocess.DEVNULL)
            subprocess.check_call(['sudo', 'apt', 'install', '-y', 'libtesseract-dev'], stdout=subprocess.DEVNULL)
            print("✅ Tesseract instalado via apt")
            return '/usr/bin/tesseract'
            
        except subprocess.CalledProcessError:
            print("❌ Erro na instalação via apt")
            print("⚠️  Tente instalar manualmente:")
            print("   sudo apt update")
            print("   sudo apt install tesseract-ocr libtesseract-dev")
            return None
    
    def install_tesseract_mac(self):
        """Instala Tesseract no macOS"""
        print("🔧 Configurando Tesseract para macOS...")
        
        # Verifica se já está instalado
        try:
            result = subprocess.run(['which', 'tesseract'], capture_output=True, text=True)
            if result.returncode == 0:
                tesseract_path = result.stdout.strip()
                print(f"✅ Tesseract encontrado em: {tesseract_path}")
                return tesseract_path
        except:
            pass
        
        print("📦 Instalando Tesseract via Homebrew...")
        
        try:
            # Verifica se Homebrew está instalado
            subprocess.check_call(['which', 'brew'], stdout=subprocess.DEVNULL)
            
            # Instala Tesseract
            subprocess.check_call(['brew', 'install', 'tesseract'], stdout=subprocess.DEVNULL)
            print("✅ Tesseract instalado via Homebrew")
            return '/usr/local/bin/tesseract'
            
        except subprocess.CalledProcessError:
            print("❌ Homebrew não encontrado ou erro na instalação")
            print("⚠️  Instale o Homebrew primeiro:")
            print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            print("   Depois execute: brew install tesseract")
            return None
    
    def setup_tesseract(self):
        """Configura Tesseract baseado no sistema operacional"""
        if self.system == "Windows":
            return self.install_tesseract_windows()
        elif self.system == "Linux":
            return self.install_tesseract_linux()
        elif self.system == "Darwin":  # macOS
            return self.install_tesseract_mac()
        else:
            print(f"❌ Sistema operacional {self.system} não suportado")
            return None
    
    def create_project_structure(self):
        """Cria a estrutura de pastas do projeto"""
        print("📁 Criando estrutura do projeto...")
        
        folders = [
            'input_images',
            'output_results',
            'logs',
            'temp',
            'config'
        ]
        
        for folder in folders:
            folder_path = self.project_dir / folder
            folder_path.mkdir(exist_ok=True)
            print(f"   ✅ Pasta criada: {folder}")
        
        # Cria arquivo .gitignore
        gitignore_content = """
# OCR Project .gitignore
*.log
*.pyc
__pycache__/
.env
temp/
*.jpg
*.jpeg
*.png
*.bmp
*.tiff
*.xlsx
*.csv
*.json
!exemplo_*.json
        """.strip()
        
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        
        print("✅ Estrutura do projeto criada")
    
    def create_config_file(self, tesseract_path):
        """Cria arquivo de configuração"""
        print("⚙️  Criando arquivo de configuração...")
        
        config = {
            "tesseract_path": tesseract_path or "",
            "input_folder": "input_images",
            "output_folder": "output_results",
            "log_level": "INFO",
            "supported_formats": [".jpg", ".jpeg", ".png", ".bmp", ".tiff"],
            "ocr_config": "--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-_",
            "business_rules": {
                "SP": "Produto de São Paulo",
                "RJ": "Produto do Rio de Janeiro",
                "MG": "Produto de Minas Gerais",
                "BR": "Produto Nacional",
                "EXP": "Produto para Exportação",
                "IMP": "Produto Importado"
            }
        }
        
        config_path = self.project_dir / 'config' / 'settings.json'
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configuração salva em: {config_path}")
    
    def create_batch_scripts(self):
        """Cria scripts em lote para facilitar o uso"""
        print("📜 Criando scripts de execução...")
        
        if self.system == "Windows":
            # Script Windows (.bat)
            batch_content = """@echo off
echo 🚀 Executando OCR Processor...
python ocr_processor.py input_images
pause
"""
            with open('executar_ocr.bat', 'w') as f:
                f.write(batch_content)
            print("   ✅ Script Windows criado: executar_ocr.bat")
        
        else:
            # Script Unix (.sh)
            bash_content = """#!/bin/bash
echo "🚀 Executando OCR Processor..."
python3 ocr_processor.py input_images
read -p "Pressione Enter para continuar..."
"""
            script_path = Path('executar_ocr.sh')
            with open(script_path, 'w') as f:
                f.write(bash_content)
            script_path.chmod(0o755)  # Torna executável
            print("   ✅ Script Unix criado: executar_ocr.sh")
    
    def create_example_files(self):
        """Cria arquivos de exemplo"""
        print("📄 Criando arquivos de exemplo...")
        
        # Exemplo de resultado JSON
        example_result = {
            "timestamp": "2025-07-27T08:00:00",
            "total_processadas": 2,
            "sucessos": 2,
            "erros": 0,
            "resultados": [
                {
                    "arquivo": "lata_001.jpg",
                    "caminho_completo": "/path/to/lata_001.jpg",
                    "texto_extraido": "LATA-12345-SP-001",
                    "texto_limpo": "LATA-12345-SP-001",
                    "observacao": "Produto de São Paulo",
                    "timestamp": "2025-07-27T08:00:00",
                    "status": "sucesso"
                },
                {
                    "arquivo": "lata_002.jpg",
                    "caminho_completo": "/path/to/lata_002.jpg",
                    "texto_extraido": "LATA-67890-BR-002",
                    "texto_limpo": "LATA-67890-BR-002",
                    "observacao": "Produto Nacional",
                    "timestamp": "2025-07-27T08:00:01",
                    "status": "sucesso"
                }
            ]
        }
        
        example_path = self.project_dir / 'output_results' / 'exemplo_resultado.json'
        with open(example_path, 'w', encoding='utf-8') as f:
            json.dump(example_result, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Exemplo JSON criado: {example_path}")
    
    def run_setup(self):
        """Executa todo o processo de configuração"""
        try:
            # Verifica Python
            if not self.check_python_version():
                return False
            
            # Instala pacotes Python
            if not self.install_python_packages():
                return False
            
            # Configura Tesseract
            tesseract_path = self.setup_tesseract()
            
            # Cria estrutura do projeto
            self.create_project_structure()
            
            # Cria configuração
            self.create_config_file(tesseract_path)
            
            # Cria scripts de execução
            self.create_batch_scripts()
            
            # Cria arquivos de exemplo
            self.create_example_files()
            
            print("\n" + "=" * 50)
            print("🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 50)
            print("📁 Estrutura do projeto:")
            print("   input_images/     ← Coloque suas imagens aqui")
            print("   output_results/   ← Resultados serão salvos aqui")
            print("   config/           ← Configurações do sistema")
            print("   logs/             ← Arquivos de log")
            print("")
            print("🚀 Como usar:")
            print("   1. Coloque imagens de latas na pasta 'input_images'")
            
            if self.system == "Windows":
                print("   2. Execute: executar_ocr.bat")
            else:
                print("   2. Execute: ./executar_ocr.sh")
            
            print("   3. Verifique os resultados em 'output_results'")
            print("")
            
            if tesseract_path:
                print(f"✅ Tesseract configurado em: {tesseract_path}")
            else:
                print("⚠️  ATENÇÃO: Configure o Tesseract manualmente")
            
            print("\n📖 Para mais informações, consulte o README.md")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro durante a configuração: {str(e)}")
            return False


def main():
    """Função principal"""
    setup = OCRSetup()
    
    if setup.run_setup():
        sys.exit(0)  # Sucesso
    else:
        sys.exit(1)  # Erro


if __name__ == "__main__":
    main()
'''

# Salva o script de setup
with open('setup.py', 'w', encoding='utf-8') as f:
    f.write(setup_script)

print("✅ Arquivo 'setup.py' criado com sucesso!")
print("🔧 Script de configuração criado com:")
print("   - Instalação automática de dependências")
print("   - Configuração do Tesseract por SO")
print("   - Criação da estrutura de pastas")
print("   - Scripts de execução facilitados")
print("   - Arquivos de exemplo")