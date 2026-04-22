# Dashboard LLM — Competências + Panorama de Mercado

Dashboard em Streamlit que combina duas narrativas:

1. **Nossas competências** — áreas de expertise, modelos dominados e casos de sucesso (totalmente configurável).
2. **Panorama do mercado** — dados ao vivo de três fontes públicas sobre LLMs: Artificial Analysis, LMSYS Chatbot Arena e Hugging Face Hub.

Pensado para apresentação a cliente externo: visual limpo, narrativa clara, dados honestos.

## Stack

- Streamlit (UI)
- Plotly (gráficos interativos)
- Pandas (manipulação de dados)
- Requests + huggingface_hub (APIs)

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuração

### 1. Editar dados da empresa

Abra `company_config.py` e ajuste:

- `COMPANY_NAME`, `COMPANY_TAGLINE`, `PRIMARY_COLOR`, `ACCENT_COLOR`, `LOGO_URL`
- `COMPETENCIES` — lista de áreas de expertise (cada uma vira um card)
- `MASTERED_MODELS` — modelos que vocês operam em produção
- `CASE_STUDIES` — cases resumidos

### 2. API keys (opcional)

A maioria das fontes funciona sem chave, mas com rate limit menor.
Copie `.env.example` para `.env` e preencha:

```env
ARTIFICIAL_ANALYSIS_API_KEY=sua_chave_aqui
HF_TOKEN=seu_token_aqui
```

- **Artificial Analysis**: cadastro gratuito em https://artificialanalysis.ai/api
- **Hugging Face**: token em https://huggingface.co/settings/tokens

Sem as chaves o dashboard continua funcionando com snapshots curados (claramente identificados na UI).

## Rodando localmente

```bash
streamlit run app.py
```

Abra http://localhost:8501 no navegador.

## Estrutura

```
llm-dashboard/
├── app.py                  # Entrypoint Streamlit — tabs e layout
├── data_sources.py         # Loaders com cache e fallback
├── company_config.py       # EDITE AQUI: dados da empresa
├── requirements.txt
├── .env.example
└── README.md
```

## Deploy

### Streamlit Community Cloud (grátis)

1. Suba o repositório no GitHub.
2. Vá em https://share.streamlit.io e conecte o repo.
3. Configure as variáveis de ambiente (`ARTIFICIAL_ANALYSIS_API_KEY`, `HF_TOKEN`) em "Secrets".

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

## Fontes de dados

| Fonte | O que traz | API pública | Frequência |
|---|---|---|---|
| Artificial Analysis | Qualidade, velocidade, preço | Sim (tier gratuito) | Diária |
| LMSYS Chatbot Arena | Ranking Elo por preferência humana | Via CSV/HF Datasets | Semanal |
| Hugging Face Hub | Popularidade de modelos open-source | Sim, gratuita | Tempo real |

## Customização avançada

- **Adicionar nova fonte**: crie uma função em `data_sources.py` seguindo o padrão (decorator `@st.cache_data`, fallback local, retorna DataFrame).
- **Novas visualizações**: adicione uma nova `st.tab` em `app.py`.
- **Cores/tema**: altere `PRIMARY_COLOR` e `ACCENT_COLOR` em `company_config.py`.

## Notas

- Cache de 1 hora por padrão. Botão "Atualizar dados" na sidebar limpa e força refresh.
- Todas as visualizações degradam graciosamente — se uma fonte cair, o resto continua funcionando.
