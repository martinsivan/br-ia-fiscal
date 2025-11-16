# br-ia-fiscal
IA para conformidade fiscal brasileira com linguagem em Python

## IA Local (Grátis)
```bash
ollama pull deepseek-coder:6.7b
ollama serve

## ESTRUTURA FINAL


br-ia-fiscal/
├── br_ia_fiscal/                 # Pacote principal
│   ├── __init__.py
│   ├── core/                     # Lógica central
│   │   ├── validator.py              # Validação XML + SEFAZ
│   │   ├── optimizer.py              # Otimização tributária
│   │   ├── monitor.py                # Monitor de mudanças legais
│   │   └── sped.py                   # Pydantic models (NFeItem, etc)
│   │   └── models.py                   
│   ├── integrations/             # APIs externas
│   │   ├── sefaz.py                  #consultar SEFAZ
│   │   ├── receita.py                #consultar CNPJ
│   ├── ai/                       # Camada de IA
│   │   ├── client.py             # Abstração de LLM
│   │   ├── prompts.py
│   │   └── grok.py / ollama.py / DeepSeek
│   ├── schemas/                  # XML Schema NF-e (XSD oficial)
│   └── utils/                    # XML, logging, helpers
├── tests/                        # 100+ testes
├── docs/                         # MkDocs
├── examples/                     # Jupyter + scripts reais
├── .github/workflows/            # CI/CD
├── pyproject.toml
├── poetry.lock
├── README.md
├── CONTRIBUTING.md
└── LICENSE (MIT)
