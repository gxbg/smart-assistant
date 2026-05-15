# 🎮 GamerZone Smart Assistant

Assistente inteligente de atendimento ao cliente para e-commerce gamer.
Desenvolvido como projeto acadêmico para o Checkpoint 03 da FIAP.

## 👥 Grupo
- Nome do integrante 1 — RM XXXXX
- Nome do integrante 2 — RM XXXXX
- Nome do integrante 3 — RM XXXXX

## 🤖 Sobre o Assistente

A **Maya** é a assistente virtual da GamerZone Store.
Ela processa mensagens de clientes usando um pipeline de 3 etapas:

1. **Classificar** — identifica tipo e urgência da mensagem
2. **Processar** — extrai dados conforme o tipo detectado
3. **Responder** — gera resposta empática e profissional

## 🏗️ Arquitetura
Mensagem do cliente
↓
🛡️ Input Guard
↓
🔍 Etapa 1: Classificar  →  ClassificacaoSchema (Pydantic)
↓
⚙️  Etapa 2: Processar   →  ProcessamentoSchema (Pydantic)
↓
✍️  Etapa 3: Responder   →  RespostaSchema (Pydantic)
↓
🛡️ Output Guard
↓
Resposta JSON validada

## ⚙️ Stack Técnica

| Tecnologia | Uso |
|-----------|-----|
| Python 3.14 | Linguagem principal |
| Ollama + llama3.2 | LLM local gratuito |
| Pydantic | Validação de JSON |
| tiktoken | Contagem de tokens |
| pandas | Análise de resultados |
| matplotlib | Geração de gráficos |
| python-dotenv | Variáveis de ambiente |

## 🚀 Como Instalar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/smart-assistant.git
cd smart-assistant
```

### 2. Crie o ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o ambiente
```bash
cp .env.example .env
```

### 5. Instale e configure o Ollama
```bash
# Baixe em: https://ollama.com
ollama pull llama3.2
ollama serve
```

### 6. Configure o .env
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
MAX_INPUT_LENGTH=500
```

## ▶️ Como Executar

### Modo Interativo
```bash
python main.py
```

### Modo Avaliação
```bash
python -m src.evaluator
```

## 📊 Resultados da Avaliação

| Métrica | Resultado |
|---------|-----------|
| Acurácia de classificação | 60% |
| Taxa de JSON válido | 100% |
| Taxa de bloqueio de ataques | 100% |
| Taxa de falso positivo | 100% |
| Consistência | 100% |

## 🛡️ Segurança — Guardrails

O sistema possui 3 camadas de proteção:

- **Input Guard** — bloqueia prompt injection, jailbreak, DAN mode
- **System Prompt defensivo** — persona Maya com regras rígidas
- **Output Guard** — verifica vazamento de informações sensíveis

## 🏗️ Frameworks de Prompt Engineering

- **Persona Pattern** — Maya com identidade e experiência definidas
- **Template Pattern** — prompts com variáveis dinâmicas por etapa
- **Recipe Pattern** — instruções passo a passo obrigatórias

## 📁 Estrutura do Projeto
smart-assistant/
├── main.py              # Ponto de entrada
├── src/
│   ├── llm_client.py    # Conexão com Ollama
│   ├── chain.py         # Pipeline 3 etapas
│   ├── schemas.py       # Modelos Pydantic
│   ├── prompts.py       # Prompts profissionais
│   ├── guardrails.py    # Sistema de segurança
│   └── evaluator.py     # Avaliação automática
├── prompts/
│   ├── system_prompt.txt
│   └── versions/        # V1, V2, V3
├── data/
│   ├── test_dataset.json
│   └── attack_dataset.json
└── output/
├── eval_results.csv
└── graficos/

## 📝 Licença
Projeto acadêmico — FIAP 2026
