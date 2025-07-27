# Criando README completo e mastigado para usuário sem conhecimento de programação
readme_content = '''# 🚀 OCR de Latas - Sistema Offline

## 📋 O que é este projeto?

Este sistema **lê automaticamente os números das suas latas** usando a **própria máquina** (sem precisar de internet após a instalação). 

Você coloca as fotos das latas numa pasta, executa um clique, e pronto: **sai uma planilha Excel organizada** com todos os dados!

---

## 🎯 Para que serve?

- ✅ Lê números/códigos das latas automaticamente
- ✅ Organiza tudo numa planilha Excel bonita
- ✅ Aplica regras automáticas (SP = São Paulo, BR = Nacional, etc.)
- ✅ Funciona **100% offline** (sem mensalidade!)
- ✅ Processa cerca de 30 fotos em poucos minutos

---

## 🛠️ INSTALAÇÃO SUPER FÁCIL

### Passo 1: Baixe o Python
1. Vai no site: https://www.python.org/downloads/
2. Clica no botão verde **"Download Python"**
3. Executa o arquivo baixado
4. ⚠️ **IMPORTANTE**: Marca a caixinha **"Add Python to PATH"**
5. Clica "Install Now"

### Passo 2: Execute a instalação automática
1. **Baixe todos os arquivos deste projeto** para uma pasta no seu computador
2. **Clique duas vezes** no arquivo `INSTALAR.bat` (Windows) ou `INSTALAR.sh` (Mac/Linux)
3. **Aguarde** - vai instalar tudo sozinho (pode demorar alguns minutos)
4. Quando aparecer "INSTALAÇÃO CONCLUÍDA", está pronto!

---

## 🚀 COMO USAR (SUPER SIMPLES!)

### 1️⃣ Coloque suas fotos
- Copie as fotos das latas para a pasta **`input_images`**
- Formatos aceitos: JPG, PNG, BMP, TIFF

### 2️⃣ Execute o processamento
- **Windows**: Clique duas vezes em `PROCESSAR_LATAS.bat`
- **Mac/Linux**: Clique duas vezes em `PROCESSAR_LATAS.sh`

### 3️⃣ Pegue os resultados
- Abra a pasta **`output_results`**
- Pronto! Sua planilha Excel está lá, organizadinha! 📊

---

## 📊 O que você vai receber?

### 📁 Arquivo Excel com 3 abas:

1. **📊 Resumo**: Estatísticas gerais
   - Quantas fotos foram processadas
   - Quantas deram certo
   - Quantas tiveram erro
   - Resumo por tipo de produto

2. **📋 Detalhes**: Tabela completa
   - Nome do arquivo da foto
   - Texto que foi lido
   - Observações automáticas
   - Status do processamento

3. **🤖 PowerAutomate**: Dados simples
   - Formato otimizado para automação
   - Ideal para Power Automate Desktop

### 📄 Arquivo CSV
- Mesmos dados em formato simples
- Ideal para importar em outros sistemas

---

## ⚙️ Configurações (se precisar)

O arquivo `config/settings.json` tem as regras automáticas:

```json
{
  "business_rules": {
    "SP": "Produto de São Paulo",
    "RJ": "Produto do Rio de Janeiro", 
    "MG": "Produto de Minas Gerais",
    "BR": "Produto Nacional",
    "EXP": "Produto para Exportação",
    "IMP": "Produto Importado"
  }
}
```

**Para adicionar novas regras**, edite este arquivo com o Bloco de Notas.

---

## 🔧 INTEGRAÇÃO COM POWER AUTOMATE

### Configuração no Power Automate Desktop:

1. **Ação: Executar Script Python**
   - Caminho do Python: `C:\\Users\\SeuUsuario\\AppData\\Local\\Programs\\Python\\Python39\\python.exe`
   - Script: `power_automate_integration.py`
   - Argumentos: `input_images --power-automate`

2. **Ação: Ler Arquivo de Texto**
   - Para capturar o resultado JSON do script

3. **Ação: Análise de JSON**  
   - Para extrair os dados do resultado

4. **Ação: Excel - Abrir Pasta de Trabalho**
   - Para abrir a planilha gerada automaticamente

### Exemplo de Fluxo Power Automate:
```
[1] Executar Script Python
    ↓
[2] Capturar Resultado JSON  
    ↓
[3] Analisar JSON
    ↓ 
[4] Abrir Excel Gerado
    ↓
[5] [Suas ações customizadas]
```

---

## 📁 Estrutura de Pastas

```
📁 OCR-Latas/
├── 📁 input_images/        ← COLOQUE SUAS FOTOS AQUI
├── 📁 output_results/      ← SEUS RESULTADOS FICAM AQUI  
├── 📁 config/              ← Configurações do sistema
├── 📁 logs/                ← Logs de execução
├── 📄 PROCESSAR_LATAS.bat  ← CLIQUE AQUI (Windows)
├── 📄 PROCESSAR_LATAS.sh   ← CLIQUE AQUI (Mac/Linux)
├── 📄 INSTALAR.bat         ← Instalação (Windows)
├── 📄 INSTALAR.sh          ← Instalação (Mac/Linux)
└── 📄 outros arquivos...
```

---

## ❓ PROBLEMAS COMUNS

### "Python não foi encontrado"
- Reinstale o Python marcando **"Add to PATH"**
- Reinicie o computador

### "Tesseract não encontrado"  
- **Windows**: Baixe em https://github.com/UB-Mannheim/tesseract/wiki
- **Linux**: Execute `sudo apt install tesseract-ocr`
- **Mac**: Execute `brew install tesseract`

### "Não conseguiu ler a lata"
- Verifique se a foto está bem focada
- Certifique-se que os números estão visíveis
- Evite reflexos e sombras

### "Excel não abre"
- Certifique-se que tem Microsoft Excel instalado
- Ou use LibreOffice (gratuito)

---

## 📞 SUPORTE

Se der algum problema:

1. 📁 Verifique a pasta `logs/` - tem detalhes do erro
2. 📸 Tire print da tela do erro
3. 📧 Mande mensagem com:
   - Print do erro
   - Exemplo de foto que não funcionou
   - Qual sistema operacional está usando

---

## 🎉 PRONTO!

Agora é só usar! 

**Lembre-se**: 
- 📁 Fotos na pasta `input_images`
- 🖱️ Clique no `PROCESSAR_LATAS`
- 📊 Planilha pronta na pasta `output_results`

**Simples assim!** 🚀

---

*Criado com ❤️ pela Confrade Tech Solutions*
'''

# Salva o README
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)

print("✅ README.md criado com instruções detalhadas!")
print("📖 Manual completo criado com:")
print("   - Instalação passo-a-passo")  
print("   - Uso super simples")
print("   - Integração Power Automate")
print("   - Solução de problemas")
print("   - Linguagem não-técnica")