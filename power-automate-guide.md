# 🤖 Guia de Integração com Power Automate Desktop

## 📋 Visão Geral

Este guia mostra como integrar o sistema OCR de Latas com o Power Automate Desktop para criar um fluxo de automação completo.

---

## 🎯 Cenário de Uso

**Objetivo**: Automatizar completamente o processo desde receber fotos por email até gerar planilhas organizadas.

**Fluxo completo**:
1. 📧 Recebe email com fotos de latas
2. 💾 Salva anexos em pasta específica  
3. 🔍 Executa OCR nas imagens
4. 📊 Gera planilha Excel automaticamente
5. 📤 Envia resultado por email ou salva no SharePoint

---

## ⚙️ Configuração Inicial

### 1. Preparar o Ambiente Python

```bash
# Configurar variáveis de ambiente no Power Automate
PYTHON_PATH = C:\Users\[SeuUsuario]\AppData\Local\Programs\Python\Python39\python.exe
PROJECT_PATH = C:\OCR-Latas\
```

### 2. Testar Integração Manual

Execute no Power Automate Desktop:

**Ação: Executar Script Python**
- **Caminho do Python**: `%PYTHON_PATH%`
- **Arquivo de Script**: `%PROJECT_PATH%power_automate_integration.py`
- **Argumentos**: `input_images --power-automate`
- **Diretório de Trabalho**: `%PROJECT_PATH%`

---

## 🔧 Exemplo de Fluxo Completo

### Fluxo: "Processar Latas do Email"

#### **Etapa 1: Monitorar Email**
```
Ação: Recuperar mensagens de email (Outlook)
- Conta: sua-conta@empresa.com
- Pasta: Caixa de Entrada
- Filtro: Assunto contém "Latas para OCR"
- Apenas não lidas: Sim
```

#### **Etapa 2: Processar Anexos**
```
Para cada email encontrado:
  ├── Ação: Obter anexos de email
  ├── Ação: Salvar anexos em pasta
  │   └── Caminho: %PROJECT_PATH%input_images\
  └── Ação: Marcar email como lido
```

#### **Etapa 3: Executar OCR**
```
Ação: Executar Script Python
├── Python: %PYTHON_PATH%
├── Script: %PROJECT_PATH%power_automate_integration.py  
├── Argumentos: input_images --power-automate
├── Diretório: %PROJECT_PATH%
└── Saída → %OCRResult%
```

#### **Etapa 4: Processar Resultado**
```
Ação: Converter texto em JSON
├── Texto JSON: %OCRResult%
└── Saída → %ResultData%

Ação: Obter propriedade JSON
├── JSON: %ResultData%
├── Propriedade: $.data.files_generated.excel_report
└── Saída → %ExcelPath%
```

#### **Etapa 5: Enviar Resultado**
```
Se %ResultData.success% = True:
  ├── Ação: Enviar email (Outlook)
  │   ├── Para: solicitante@empresa.com
  │   ├── Assunto: "OCR Concluído - %ResultData.data.total_images% latas processadas"
  │   ├── Corpo: "Relatório em anexo. Taxa de sucesso: %ResultData.data.success_rate%%"
  │   └── Anexos: %ExcelPath%
  └── Ação: Limpar pasta input_images
Senão:
  └── Ação: Enviar email de erro
```

---

## 📊 Estrutura do JSON de Retorno

O script retorna um JSON estruturado:

```json
{
  "success": true,
  "message": "Processamento OCR concluído com sucesso",
  "data": {
    "timestamp": "2025-07-27T08:00:00",
    "total_images": 5,
    "successful_ocr": 4,
    "failed_ocr": 1,
    "success_rate": 80.0,
    "files_generated": {
      "json_results": "C:\\OCR-Latas\\output_results\\ocr_results_20250727_080000.json",
      "excel_report": "C:\\OCR-Latas\\output_results\\relatorio_ocr_latas_20250727_080000.xlsx",
      "csv_data": "C:\\OCR-Latas\\output_results\\dados_ocr_latas_20250727_080000.csv"
    }
  }
}
```

### Propriedades Úteis:

- `$.success` → True/False (sucesso geral)
- `$.data.total_images` → Número total de imagens
- `$.data.successful_ocr` → OCRs bem-sucedidos  
- `$.data.success_rate` → Taxa de sucesso (%)
- `$.data.files_generated.excel_report` → Caminho do Excel
- `$.data.files_generated.csv_data` → Caminho do CSV

---

## 🔄 Fluxos Alternativos

### Fluxo Simples: "OCR Manual"

Para uso pontual:

```
1. Ação: Exibir caixa de diálogo de entrada
   └── "Coloque as fotos na pasta input_images e clique OK"

2. Ação: Executar Script Python
   └── [configuração padrão]

3. Ação: Abrir arquivo
   └── Caminho: %ExcelPath%
```

### Fluxo Avançado: "OCR com SharePoint"

Para integração corporativa:

```
1. Monitorar pasta do SharePoint
2. Baixar novas imagens
3. Executar OCR  
4. Upload do Excel para SharePoint
5. Notificar equipe via Teams
```

---

## 🛠️ Configuração de Variáveis

### Variáveis Globais Recomendadas:

| Nome | Valor | Descrição |
|------|-------|-----------|
| `PYTHON_PATH` | `C:\Users\...\python.exe` | Caminho do Python |
| `PROJECT_PATH` | `C:\OCR-Latas\` | Pasta do projeto |
| `INPUT_FOLDER` | `%PROJECT_PATH%input_images` | Pasta de entrada |
| `OUTPUT_FOLDER` | `%PROJECT_PATH%output_results` | Pasta de saída |
| `EMAIL_REMETENTE` | `ocr@empresa.com` | Email para envios |

---

## 🔍 Tratamento de Erros

### Verificações Recomendadas:

```
Ação: Se arquivo existe
├── Caminho: %PYTHON_PATH%
├── Senão → Exibir erro: "Python não instalado"

Ação: Se pasta existe  
├── Caminho: %PROJECT_PATH%
├── Senão → Exibir erro: "Projeto OCR não encontrado"

Ação: Verificar JSON
├── Se %OCRResult% contém "success": false
├── Então → Processar erro e notificar
```

### Log de Execução:

```
Ação: Escrever em arquivo de texto
├── Arquivo: %PROJECT_PATH%logs\power_automate.log
├── Texto: "%Datetime% - Processadas %TotalImages% imagens - Sucesso: %SuccessRate%%"
└── Codificação: UTF-8
```

---

## 📋 Checklist de Implementação

### ✅ Pré-requisitos:
- [ ] Python instalado e configurado
- [ ] Projeto OCR instalado (`INSTALAR.bat` executado)
- [ ] Tesseract OCR funcionando
- [ ] Power Automate Desktop licenciado
- [ ] Permissões de pasta configuradas

### ✅ Configuração:
- [ ] Variáveis de ambiente definidas
- [ ] Teste manual do script Python executado
- [ ] Integração básica funcionando
- [ ] Tratamento de erros implementado

### ✅ Produção:
- [ ] Fluxo completo testado com dados reais
- [ ] Monitoramento e logs configurados
- [ ] Plano de backup das imagens
- [ ] Documentação para usuários finais

---

## 🚀 Dicas de Performance

### Para Volume Alto (100+ imagens/dia):

1. **Processamento em Lote**:
   ```
   Para cada 10 imagens:
   └── Executar OCR
   └── Aguardar conclusão
   └── Processar próximo lote
   ```

2. **Limpeza Automática**:
   ```
   Após sucesso:
   ├── Mover imagens processadas para pasta "Processadas"
   ├── Limpar pasta temporária
   └── Compactar arquivos antigos
   ```

3. **Monitoramento**:
   ```
   A cada execução:
   ├── Registrar estatísticas
   ├── Verificar espaço em disco  
   └── Alertar se taxa de erro > 20%
   ```

---

## 🎯 Casos de Uso Avançados

### 1. **Validação Automática**
- Verificar se números estão no padrão esperado
- Alertar sobre latas com códigos inválidos
- Solicitar revisão manual para casos duvidosos

### 2. **Integração com ERP**
- Consultar base de dados para validar códigos
- Atualizar status de produção automaticamente
- Gerar relatórios gerenciais

### 3. **Dashboard em Tempo Real**
- Power BI conectado aos CSVs gerados
- Métricas de produtividade da linha
- Alertas automáticos por Teams/WhatsApp

---

## 📞 Suporte e Manutenção

### Logs para Diagnóstico:
- `logs/ocr_processor.log` → Detalhes do OCR
- `logs/power_automate_integration.log` → Integração PA
- `logs/power_automate.log` → Log do fluxo PA

### Monitoramento Recomendado:
- Taxa de sucesso > 85%
- Tempo de processamento < 2min por lote
- Espaço em disco disponível > 1GB
- CPU durante OCR < 80%

### Contato Técnico:
- 📧 Email: suporte@confrade-tech.com
- 📱 WhatsApp: (11) 99999-9999  
- 🌐 Portal: suporte.confrade-tech.com

---

*🎉 Agora você tem um sistema completo de OCR integrado ao Power Automate, 100% gratuito e altamente customizável!*