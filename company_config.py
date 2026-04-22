"""
Configurações da empresa — edite este arquivo para personalizar o dashboard.
Toda a parte de "Nossas Competências" é lida daqui.
"""

# =========================================================================
# IDENTIDADE — paleta e tipografia alinhadas ao site maximizia.com.br
# =========================================================================
COMPANY_NAME = "MaximizIA"
COMPANY_TAGLINE = "IA aplicada a negócios — sem hype, com qualidade e resultado mensurável."
COMPANY_SITE_URL = "https://www.maximizia.com.br"
COMPANY_WHATSAPP_URL = "https://wa.me/5511942408369"
COMPANY_LINKEDIN_URL = "https://www.linkedin.com/company/maximizia"
LOGO_URL = ""  # logo do site é tipográfico — renderizado via CSS no app.py

# Paleta (idêntica ao tailwind-config do site)
COLOR_VOID = "#08080a"         # fundo principal (quase preto)
COLOR_SURFACE = "#0f0e14"      # superfícies secundárias (cards, sidebar)
COLOR_MIST = "#e8e6e3"         # texto principal
COLOR_MIST_DIM = "rgba(232, 230, 227, 0.55)"
COLOR_BORDER = "rgba(255, 255, 255, 0.08)"

PRIMARY_COLOR = "#a855f7"      # roxo (accent do site — usado em destaques da marca)
PRIMARY_MUTED = "#7c3aed"
ACCENT_COLOR = "#ea580c"       # laranja (CTA do site — usado em botões/chamadas)
ACCENT_HOVER = "#f97316"

# =========================================================================
# COMPETÊNCIAS DA EQUIPE
# Cada item vira um card na aba "Nossas Competências"
# =========================================================================
COMPETENCIES = [
    {
        "area": "Descoberta e priorização de casos de uso",
        "description": "Identificamos onde IA gera ROI real e descartamos o que é vitrine. Começamos por problema de negócio, não por tecnologia.",
        "level": 95,
        "projects": 28,
    },
    {
        "area": "Arquitetura de soluções com LLMs",
        "description": "Desenho técnico honesto: escolha do modelo certo para cada tarefa, balanceando qualidade, custo, latência e risco.",
        "level": 92,
        "projects": 34,
    },
    {
        "area": "RAG e integração com dados proprietários",
        "description": "Conectamos LLMs aos dados reais do cliente com recuperação, re-ranking e citação de fontes — zero alucinação aceita em produção.",
        "level": 93,
        "projects": 31,
    },
    {
        "area": "Automação de processos com agentes",
        "description": "Agentes que executam tarefas repetitivas com supervisão humana clara. Escopo enxuto, hand-off bem definido, auditabilidade.",
        "level": 85,
        "projects": 17,
    },
    {
        "area": "Avaliação, qualidade e observabilidade",
        "description": "Benchmarks customizados por caso de uso, LLM-as-judge, monitoramento de custo e deriva. Se não mede, não vai pra produção.",
        "level": 88,
        "projects": 22,
    },
    {
        "area": "Segurança, LGPD e governança",
        "description": "Guardrails, proteção contra prompt injection, políticas de retenção e trilha de auditoria. IA que passa no jurídico do cliente.",
        "level": 87,
        "projects": 14,
    },
]

# =========================================================================
# MODELOS QUE DOMINAMOS
# =========================================================================
MASTERED_MODELS = [
    {"model": "Claude Opus 4.6", "provider": "Anthropic", "use_cases": "Raciocínio complexo, análise de documentos longos, decisões de alto valor", "experience": "Alto"},
    {"model": "Claude Sonnet 4.6", "provider": "Anthropic", "use_cases": "Carro-chefe de produção — custo-benefício e confiabilidade", "experience": "Alto"},
    {"model": "GPT-4o", "provider": "OpenAI", "use_cases": "Multimodal, agentes, integrações amplas", "experience": "Alto"},
    {"model": "GPT-4.1", "provider": "OpenAI", "use_cases": "Contexto longo, código, análise de planilhas", "experience": "Médio"},
    {"model": "Gemini 2.5 Pro", "provider": "Google", "use_cases": "Documentos extensos, multimodal nativo, Google Workspace", "experience": "Médio"},
    {"model": "Llama 3.3 70B", "provider": "Meta (open-source)", "use_cases": "Deploy on-premises, dados sensíveis, custo previsível", "experience": "Alto"},
    {"model": "Mistral Large", "provider": "Mistral", "use_cases": "Alternativa europeia, soberania de dados, multilíngue", "experience": "Médio"},
    {"model": "DeepSeek V3", "provider": "DeepSeek (open-source)", "use_cases": "Tarefas de raciocínio e código a custo muito baixo", "experience": "Médio"},
]

# =========================================================================
# CASOS DE SUCESSO
# =========================================================================
SHOW_CASE_STUDIES = True
CASE_STUDIES = [
    {
        "title": "Automação de análise contratual",
        "client_sector": "Jurídico corporativo",
        "outcome": "Triagem de cláusulas de risco em 5 min (vs. 2 horas). 100% com citação do trecho original para revisão humana.",
        "models_used": ["Claude Sonnet 4.6", "Embeddings OpenAI"],
    },
    {
        "title": "Assistente interno de dúvidas operacionais",
        "client_sector": "Indústria",
        "outcome": "45% de redução em tickets ao suporte interno, com respostas ancoradas em manuais oficiais e log de auditoria.",
        "models_used": ["Claude Sonnet 4.6", "Llama 3.3 70B (ambiente restrito)"],
    },
    {
        "title": "Extração estruturada de documentos fiscais",
        "client_sector": "Financeiro / BPO",
        "outcome": "Pipeline processando 10k+ documentos/dia com 98% de precisão e 60% de redução no custo operacional.",
        "models_used": ["Claude Opus 4.6", "Gemini 2.5 Pro (visão)"],
    },
]
