"""
Dashboard LLM — Competências internas + Panorama do mercado
Público-alvo: cliente externo
Visual alinhado ao site maximizia.com.br (fundo void #08080a + paleta roxo/laranja)
Stack: Streamlit + Plotly + Pandas
"""
import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.io as pio
import streamlit as st
from dotenv import load_dotenv

import company_config as cfg
from data_sources import (
    load_artificial_analysis,
    load_hf_leaderboard,
    load_lmsys_arena,
)

load_dotenv()

# =========================================================================
# PAGE CONFIG
# =========================================================================
st.set_page_config(
    page_title=f"{cfg.COMPANY_NAME} · Panorama de LLMs",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================================
# PLOTLY — tema escuro padrão
# =========================================================================
PLOT_FONT = "Inter, system-ui, sans-serif"
PLOT_GRID = "rgba(255,255,255,0.06)"
PLOT_AXIS = "rgba(232,230,227,0.55)"

pio.templates["maximizia"] = pio.templates["plotly_dark"]
pio.templates["maximizia"].layout.update(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family=PLOT_FONT, color=cfg.COLOR_MIST, size=13),
    colorway=[
        cfg.PRIMARY_COLOR, cfg.ACCENT_COLOR, "#22d3ee", "#f472b6",
        "#34d399", "#fbbf24", "#60a5fa", "#c084fc",
    ],
    xaxis=dict(gridcolor=PLOT_GRID, zerolinecolor=PLOT_GRID, linecolor=PLOT_GRID, tickcolor=PLOT_AXIS),
    yaxis=dict(gridcolor=PLOT_GRID, zerolinecolor=PLOT_GRID, linecolor=PLOT_GRID, tickcolor=PLOT_AXIS),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)
pio.templates.default = "maximizia"


def style_fig(fig):
    """Aplica ajustes finais a qualquer fig Plotly."""
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        hoverlabel=dict(
            bgcolor="#0f0e14",
            bordercolor=cfg.PRIMARY_COLOR,
            font=dict(color=cfg.COLOR_MIST, family=PLOT_FONT),
        ),
    )
    return fig


# =========================================================================
# CSS — tema void/mist/roxo/laranja + tipografia do site
# =========================================================================
CUSTOM_CSS = f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"], .stApp {{
    background: {cfg.COLOR_VOID} !important;
    color: {cfg.COLOR_MIST};
    font-family: 'Inter', system-ui, sans-serif;
  }}

  .stApp {{
    background:
      radial-gradient(ellipse at 15% -10%, rgba(168,85,247,0.12), transparent 55%),
      radial-gradient(ellipse at 110% 20%, rgba(234,88,12,0.10), transparent 55%),
      {cfg.COLOR_VOID} !important;
  }}

  .block-container {{ padding-top: 3.5rem; max-width: 1400px; }}

  /* Header nativo do Streamlit transparente para combinar com o fundo void */
  header[data-testid="stHeader"] {{
    background: rgba(8,8,10,0.55) !important;
    backdrop-filter: blur(12px);
    border-bottom: 1px solid {cfg.COLOR_BORDER};
  }}
  header[data-testid="stHeader"] button[kind="header"],
  header[data-testid="stHeader"] svg {{
    color: {cfg.COLOR_MIST} !important;
    fill: {cfg.COLOR_MIST} !important;
  }}

  h1, h2, h3, h4 {{
    font-family: 'Space Grotesk', 'Inter', system-ui, sans-serif;
    color: {cfg.COLOR_MIST};
    letter-spacing: -0.02em;
    font-weight: 600;
  }}

  p, span, label, div {{ color: {cfg.COLOR_MIST}; }}

  a {{ color: {cfg.PRIMARY_COLOR}; text-decoration: none; }}
  a:hover {{ color: {cfg.ACCENT_COLOR}; }}

  /* ---------- Top bar com botão "voltar para o site" ---------- */
  .topbar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 0 1.25rem 0;
    border-bottom: 1px solid {cfg.COLOR_BORDER};
    margin-bottom: 1.5rem;
    gap: 1rem;
    flex-wrap: wrap;
  }}
  .topbar > div:first-child {{
    display: flex; align-items: center; flex-wrap: wrap; gap: 0.75rem;
    line-height: 1.4;
  }}
  .brand {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1.5rem;
    letter-spacing: -0.02em;
  }}
  .brand .orange {{ color: {cfg.ACCENT_COLOR}; }}
  .brand .purple {{ color: {cfg.PRIMARY_COLOR}; }}
  .brand .sep {{
    display: inline-block;
    margin: 0 0.75rem;
    color: rgba(232,230,227,0.25);
  }}
  .brand .crumb {{
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(232,230,227,0.45);
    font-weight: 500;
  }}
  .topbar-actions {{ display: flex; gap: 0.6rem; align-items: center; }}
  .btn-cta, .btn-ghost {{
    display: inline-flex; align-items: center; gap: 0.5rem;
    padding: 0.6rem 1.1rem;
    font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.12em;
    border-radius: 3px;
    transition: all 0.2s ease;
    text-decoration: none !important;
  }}
  .btn-cta {{
    background: {cfg.ACCENT_COLOR};
    color: {cfg.COLOR_VOID} !important;
    border: 1px solid {cfg.ACCENT_COLOR};
  }}
  .btn-cta:hover {{
    background: {cfg.ACCENT_HOVER};
    border-color: {cfg.ACCENT_HOVER};
  }}
  .btn-ghost {{
    background: rgba(255,255,255,0.02);
    color: {cfg.COLOR_MIST} !important;
    border: 1px solid rgba(255,255,255,0.15);
  }}
  .btn-ghost:hover {{
    border-color: rgba(168,85,247,0.55);
    color: {cfg.PRIMARY_COLOR} !important;
  }}

  /* ---------- Hero ---------- */
  .hero {{
    position: relative;
    padding: 2.5rem 2rem 2.75rem 2rem;
    border-radius: 6px;
    border: 1px solid {cfg.COLOR_BORDER};
    background:
      linear-gradient(135deg, rgba(168,85,247,0.14) 0%, rgba(234,88,12,0.10) 100%),
      rgba(255,255,255,0.02);
    backdrop-filter: blur(24px);
    margin-bottom: 2rem;
    overflow: hidden;
  }}
  .hero::before {{
    content: "";
    position: absolute; inset: 0;
    background: radial-gradient(circle at 85% 10%, rgba(168,85,247,0.25), transparent 45%);
    pointer-events: none;
  }}
  .hero-badge {{
    display: inline-flex; align-items: center; gap: 0.5rem;
    padding: 0.35rem 0.9rem;
    border: 1px solid rgba(168,85,247,0.35);
    border-radius: 999px;
    font-size: 0.68rem; font-weight: 500;
    letter-spacing: 0.2em; text-transform: uppercase;
    color: rgba(232,230,227,0.7);
    margin-bottom: 1.25rem;
  }}
  .hero-badge .dot {{
    width: 6px; height: 6px; border-radius: 50%;
    background: {cfg.PRIMARY_COLOR};
    box-shadow: 0 0 8px {cfg.PRIMARY_COLOR};
  }}
  .hero h1 {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.4rem;
    font-weight: 600;
    margin: 0 0 0.75rem 0;
    color: {cfg.COLOR_MIST};
  }}
  .hero p {{
    font-size: 1.05rem;
    color: rgba(232,230,227,0.65);
    font-weight: 300;
    max-width: 720px;
    line-height: 1.6;
    margin: 0;
  }}

  /* ---------- Métricas ---------- */
  [data-testid="stMetric"] {{
    background: rgba(255,255,255,0.03);
    border: 1px solid {cfg.COLOR_BORDER};
    padding: 1.1rem 1.25rem;
    border-radius: 4px;
    backdrop-filter: blur(12px);
  }}
  [data-testid="stMetric"] label {{
    color: rgba(232,230,227,0.5) !important;
    font-size: 0.7rem !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 500;
  }}
  [data-testid="stMetricValue"] {{
    color: {cfg.COLOR_MIST} !important;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
  }}

  /* ---------- Cards ---------- */
  .competency-card {{
    background: rgba(255,255,255,0.03);
    border: 1px solid {cfg.COLOR_BORDER};
    border-radius: 4px;
    padding: 1.4rem 1.25rem 1.1rem 1.25rem;
    height: 100%;
    transition: border-color 0.25s ease;
  }}
  .competency-card:hover {{ border-color: rgba(168,85,247,0.35); }}
  .competency-card h4 {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.05rem;
    margin-top: 0; margin-bottom: 0.6rem;
    color: {cfg.COLOR_MIST};
  }}
  .competency-card p {{
    color: rgba(232,230,227,0.55);
    font-size: 0.88rem;
    line-height: 1.55;
    font-weight: 300;
    min-height: 72px;
  }}
  .case-card {{
    background: rgba(255,255,255,0.03);
    border: 1px solid {cfg.COLOR_BORDER};
    border-left: 3px solid {cfg.ACCENT_COLOR};
    padding: 1rem 1.25rem;
    border-radius: 3px;
    margin-bottom: 0.75rem;
  }}
  .case-card strong {{ color: {cfg.COLOR_MIST}; font-family: 'Space Grotesk', sans-serif; }}
  .case-card p {{ color: rgba(232,230,227,0.7); margin: 0.4rem 0; font-weight: 300; }}
  .case-card small {{ color: rgba(232,230,227,0.4); }}

  /* ---------- Tabs ---------- */
  .stTabs [data-baseweb="tab-list"] {{
    gap: 0.25rem;
    border-bottom: 1px solid {cfg.COLOR_BORDER};
  }}
  .stTabs [data-baseweb="tab"] {{
    background: transparent !important;
    color: rgba(232,230,227,0.5) !important;
    font-size: 0.8rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.75rem 1.1rem;
    border-radius: 3px 3px 0 0;
  }}
  .stTabs [aria-selected="true"] {{
    color: {cfg.COLOR_MIST} !important;
    background: rgba(168,85,247,0.08) !important;
    border-bottom: 2px solid {cfg.PRIMARY_COLOR} !important;
  }}

  /* ---------- Sidebar ---------- */
  section[data-testid="stSidebar"] {{
    background: {cfg.COLOR_SURFACE} !important;
    border-right: 1px solid {cfg.COLOR_BORDER};
  }}
  section[data-testid="stSidebar"] * {{ color: {cfg.COLOR_MIST}; }}
  section[data-testid="stSidebar"] .stButton button {{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.15);
    color: {cfg.COLOR_MIST};
    width: 100%;
    border-radius: 3px;
    text-transform: uppercase;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    font-weight: 600;
  }}
  section[data-testid="stSidebar"] .stButton button:hover {{
    border-color: rgba(168,85,247,0.5);
    color: {cfg.PRIMARY_COLOR};
  }}

  /* ---------- Botões de link (link_button) ---------- */
  a[data-testid="stBaseLinkButton-primary"],
  a[data-testid="stBaseLinkButton-secondary"] {{
    text-transform: uppercase;
    font-size: 0.72rem !important;
    letter-spacing: 0.12em;
    font-weight: 700 !important;
    border-radius: 3px !important;
  }}
  a[data-testid="stBaseLinkButton-primary"] {{
    background: {cfg.ACCENT_COLOR} !important;
    border-color: {cfg.ACCENT_COLOR} !important;
    color: {cfg.COLOR_VOID} !important;
  }}
  a[data-testid="stBaseLinkButton-primary"]:hover {{
    background: {cfg.ACCENT_HOVER} !important;
    border-color: {cfg.ACCENT_HOVER} !important;
  }}

  /* ---------- DataFrame ---------- */
  [data-testid="stDataFrame"] {{
    background: rgba(255,255,255,0.02);
    border: 1px solid {cfg.COLOR_BORDER};
    border-radius: 4px;
  }}

  /* ---------- Info box ---------- */
  [data-testid="stAlert"] {{
    background: rgba(168,85,247,0.08) !important;
    border: 1px solid rgba(168,85,247,0.25) !important;
    border-radius: 4px;
  }}

  /* ---------- Caption ---------- */
  [data-testid="stCaptionContainer"] {{ color: rgba(232,230,227,0.45) !important; }}

  /* ---------- Footer MaximizIA ---------- */
  .mx-footer {{
    margin-top: 3rem;
    padding: 1.75rem 0 1rem 0;
    border-top: 1px solid {cfg.COLOR_BORDER};
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
  }}
  .mx-footer .left {{
    font-size: 0.75rem;
    color: rgba(232,230,227,0.45);
    letter-spacing: 0.08em;
  }}
  .mx-footer .right {{ display: flex; gap: 0.75rem; align-items: center; }}
  .mx-footer a.link {{
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: rgba(232,230,227,0.55) !important;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding-bottom: 2px;
    font-weight: 500;
  }}
  .mx-footer a.link:hover {{ color: {cfg.PRIMARY_COLOR} !important; border-bottom-color: {cfg.PRIMARY_COLOR}; }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =========================================================================
# TOP BAR — logo + botões de navegação para o site
# =========================================================================
st.markdown(
    f"""
    <div class="topbar">
      <div>
        <a href="{cfg.COMPANY_SITE_URL}" target="_blank" class="brand">
          <span class="orange">Maximiz</span><span class="purple">IA</span>
        </a>
        <span class="sep">/</span>
        <span class="crumb">Panorama de LLMs</span>
      </div>
      <div class="topbar-actions">
        <a href="{cfg.COMPANY_SITE_URL}" target="_blank" class="btn-ghost">← Voltar ao site</a>
        <a href="{cfg.COMPANY_WHATSAPP_URL}" target="_blank" class="btn-cta">Falar com a gente</a>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================================
# HERO
# =========================================================================
st.markdown(
    f"""
    <div class="hero">
      <div class="hero-badge"><span class="dot"></span> Consultoria em IA · {datetime.now().strftime('%b %Y').capitalize()}</div>
      <h1>{cfg.COMPANY_NAME} · Panorama de LLMs</h1>
      <p>{cfg.COMPANY_TAGLINE}</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================================
# SIDEBAR
# =========================================================================
with st.sidebar:
    st.markdown(
        f"""
        <div style="padding: 0.5rem 0 1rem 0;">
          <div class="brand" style="font-size:1.35rem">
            <span class="orange">Maximiz</span><span class="purple">IA</span>
          </div>
          <div style="color:rgba(232,230,227,0.45); font-size:0.72rem;
                      letter-spacing:0.14em; text-transform:uppercase;
                      margin-top:0.35rem;">
            Dashboard executivo
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("**Fontes consultadas**")
    st.markdown(
        "- Artificial Analysis\n"
        "- LMSYS Chatbot Arena\n"
        "- Hugging Face Hub"
    )
    st.markdown("---")
    st.caption(f"Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    if st.button("Atualizar dados"):
        st.cache_data.clear()
        st.rerun()
    st.markdown("---")
    st.link_button("Ir para maximizia.com.br ↗", cfg.COMPANY_SITE_URL, use_container_width=True)


# =========================================================================
# TABS
# =========================================================================
tab_overview, tab_comp, tab_market, tab_compare, tab_about = st.tabs([
    "Visão Geral",
    "Nossas Competências",
    "Panorama do Mercado",
    "Comparativo por Fonte",
    "Sobre os dados",
])


# =========================================================================
# TAB: VISÃO GERAL
# =========================================================================
with tab_overview:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Competências", len(cfg.COMPETENCIES))
    col2.metric("Modelos dominados", len(cfg.MASTERED_MODELS))
    total_projects = sum(c["projects"] for c in cfg.COMPETENCIES)
    col3.metric("Projetos entregues", total_projects)
    col4.metric("Provedores", len({m["provider"] for m in cfg.MASTERED_MODELS}))

    st.markdown("### Nosso posicionamento no mercado")
    st.caption(
        "Operamos com modelos de todos os principais provedores, "
        "escolhendo a combinação certa para cada caso de uso."
    )

    df_aa = load_artificial_analysis()

    mastered_names = {m["model"] for m in cfg.MASTERED_MODELS}
    df_aa["dominamos"] = df_aa["model"].isin(mastered_names).map(
        {True: "Modelos que dominamos", False: "Outros do mercado"}
    )

    fig = px.scatter(
        df_aa.dropna(subset=["quality_index", "price_output_per_1m"]),
        x="price_output_per_1m",
        y="quality_index",
        color="dominamos",
        size="output_speed_tps",
        hover_name="model",
        hover_data={"provider": True, "context_window": True, "dominamos": False},
        labels={
            "price_output_per_1m": "Preço de saída (USD por 1M tokens)",
            "quality_index": "Índice de qualidade (Artificial Analysis)",
            "output_speed_tps": "Tokens/s",
        },
        color_discrete_map={
            "Modelos que dominamos": cfg.ACCENT_COLOR,
            "Outros do mercado": "rgba(232,230,227,0.22)",
        },
        log_x=True,
        height=520,
    )
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02))
    st.plotly_chart(style_fig(fig), use_container_width=True)
    st.caption(
        "Tamanho do círculo = velocidade de geração (tokens/s). "
        "Quanto mais alto e à esquerda, melhor o custo-benefício."
    )


# =========================================================================
# TAB: NOSSAS COMPETÊNCIAS
# =========================================================================
with tab_comp:
    st.markdown("## Onde temos expertise comprovada")
    st.caption(
        "Cada área abaixo representa capacidades entregues em projetos reais, "
        "com times e processos dedicados."
    )

    cols = st.columns(3)
    for i, comp in enumerate(cfg.COMPETENCIES):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="competency-card">
                  <h4>{comp['area']}</h4>
                  <p>{comp['description']}</p>
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-top:0.75rem">
                    <span style="color:rgba(232,230,227,0.4);font-size:0.78rem;letter-spacing:0.05em">
                      {comp['projects']} projetos
                    </span>
                    <span style="color:{cfg.ACCENT_COLOR};font-family:'Space Grotesk',sans-serif;
                                 font-weight:600;font-size:1rem">{comp['level']}%</span>
                  </div>
                  <div style="background:rgba(255,255,255,0.06);border-radius:99px;height:4px;margin-top:6px">
                    <div style="background:linear-gradient(90deg,{cfg.PRIMARY_COLOR},{cfg.ACCENT_COLOR});
                                width:{comp['level']}%;height:100%;border-radius:99px"></div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("### Modelos que operamos em produção")
    df_models = pd.DataFrame(cfg.MASTERED_MODELS)
    st.dataframe(
        df_models,
        use_container_width=True,
        hide_index=True,
        column_config={
            "model": "Modelo",
            "provider": "Provedor",
            "use_cases": "Casos de uso",
            "experience": st.column_config.TextColumn("Experiência", width="small"),
        },
    )

    if cfg.SHOW_CASE_STUDIES and cfg.CASE_STUDIES:
        st.markdown("---")
        st.markdown("### Casos de sucesso")
        for cs in cfg.CASE_STUDIES:
            st.markdown(
                f"""
                <div class="case-card">
                  <strong>{cs['title']}</strong>
                  <span style="color:rgba(232,230,227,0.4);margin-left:0.5rem">· {cs['client_sector']}</span>
                  <p>{cs['outcome']}</p>
                  <small>Modelos: {", ".join(cs['models_used'])}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )


# =========================================================================
# TAB: PANORAMA DO MERCADO
# =========================================================================
with tab_market:
    st.markdown("## O estado atual dos LLMs")
    st.caption(
        "Dados agregados de três fontes independentes. "
        "Atualizamos automaticamente a cada hora."
    )

    df_aa = load_artificial_analysis()

    providers = sorted(df_aa["provider"].dropna().unique().tolist())
    selected_providers = st.multiselect(
        "Filtrar por provedor:",
        providers,
        default=providers,
    )
    df_filtered = df_aa[df_aa["provider"].isin(selected_providers)]

    c1, c2, c3 = st.columns(3)
    c1.metric(
        "Modelo mais inteligente",
        df_filtered.nlargest(1, "quality_index").iloc[0]["model"] if not df_filtered.empty else "—",
    )
    c2.metric(
        "Mais rápido (tokens/s)",
        df_filtered.nlargest(1, "output_speed_tps").iloc[0]["model"] if not df_filtered.empty else "—",
    )
    cheapest = df_filtered.nsmallest(1, "price_output_per_1m")
    c3.metric(
        "Mais barato (output)",
        cheapest.iloc[0]["model"] if not cheapest.empty else "—",
        f"USD {cheapest.iloc[0]['price_output_per_1m']:.2f} / 1M" if not cheapest.empty else None,
    )

    st.markdown("### Qualidade vs. Preço")
    fig = px.scatter(
        df_filtered.dropna(subset=["quality_index", "price_output_per_1m"]),
        x="price_output_per_1m",
        y="quality_index",
        color="provider",
        size="output_speed_tps",
        hover_name="model",
        labels={
            "price_output_per_1m": "USD por 1M tokens (saída)",
            "quality_index": "Qualidade",
        },
        log_x=True,
        height=480,
    )
    st.plotly_chart(style_fig(fig), use_container_width=True)

    st.markdown("### Tabela completa")
    display_cols = ["model", "provider", "quality_index", "output_speed_tps",
                    "price_input_per_1m", "price_output_per_1m", "context_window"]
    st.dataframe(
        df_filtered[display_cols].sort_values("quality_index", ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "model": "Modelo",
            "provider": "Provedor",
            "quality_index": st.column_config.ProgressColumn(
                "Qualidade", min_value=0, max_value=100, format="%d"
            ),
            "output_speed_tps": st.column_config.NumberColumn("Tokens/s", format="%.0f"),
            "price_input_per_1m": st.column_config.NumberColumn("$ input / 1M", format="$%.2f"),
            "price_output_per_1m": st.column_config.NumberColumn("$ output / 1M", format="$%.2f"),
            "context_window": st.column_config.NumberColumn("Context", format="%d"),
        },
    )
    st.caption(f"Fonte: {df_filtered['_source'].iloc[0] if not df_filtered.empty else '—'}")


# =========================================================================
# TAB: COMPARATIVO POR FONTE
# =========================================================================
with tab_compare:
    st.markdown("## Três visões independentes do mesmo mercado")

    colA, colB = st.columns(2)

    with colA:
        st.markdown("### LMSYS Chatbot Arena")
        st.caption("Ranking baseado em preferência humana (Elo)")
        df_arena = load_lmsys_arena()
        top_arena = df_arena.nlargest(15, "elo") if "elo" in df_arena.columns else df_arena.head(15)
        fig = px.bar(
            top_arena,
            x="elo",
            y="model",
            orientation="h",
            color="elo",
            color_continuous_scale=["rgba(168,85,247,0.25)", cfg.PRIMARY_COLOR],
            height=500,
        )
        fig.update_layout(
            yaxis={"categoryorder": "total ascending"},
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title="Elo",
            yaxis_title="",
        )
        st.plotly_chart(style_fig(fig), use_container_width=True)
        st.caption(f"Fonte: {df_arena['_source'].iloc[0] if '_source' in df_arena.columns else 'LMSYS'}")

    with colB:
        st.markdown("### Hugging Face Hub")
        st.caption("Modelos open-source mais utilizados pela comunidade")
        df_hf = load_hf_leaderboard()
        top_hf = df_hf.nlargest(15, "downloads") if "downloads" in df_hf.columns else df_hf.head(15)
        fig = px.bar(
            top_hf,
            x="downloads",
            y="model",
            orientation="h",
            color="downloads",
            color_continuous_scale=["rgba(234,88,12,0.25)", cfg.ACCENT_COLOR],
            height=500,
        )
        fig.update_layout(
            yaxis={"categoryorder": "total ascending"},
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title="Downloads (mês)",
            yaxis_title="",
        )
        st.plotly_chart(style_fig(fig), use_container_width=True)
        st.caption(f"Fonte: {df_hf['_source'].iloc[0] if '_source' in df_hf.columns else 'HF Hub'}")

    st.markdown("---")
    st.markdown("### Artificial Analysis — síntese de qualidade, velocidade e preço")
    df_aa = load_artificial_analysis()
    fig = px.scatter(
        df_aa.dropna(subset=["quality_index", "output_speed_tps"]),
        x="output_speed_tps",
        y="quality_index",
        color="provider",
        size="price_output_per_1m",
        hover_name="model",
        labels={
            "output_speed_tps": "Velocidade (tokens/s)",
            "quality_index": "Qualidade",
        },
        height=480,
    )
    st.plotly_chart(style_fig(fig), use_container_width=True)
    st.caption(f"Fonte: {df_aa['_source'].iloc[0]}. Tamanho do círculo = preço de saída.")


# =========================================================================
# TAB: SOBRE
# =========================================================================
with tab_about:
    st.markdown("## Sobre este dashboard")
    st.markdown(
        f"""
        Este painel agrega informações públicas para dar um panorama honesto e
        atualizado do mercado de LLMs. Todas as fontes abaixo são consultadas
        programaticamente — não há curadoria manual de rankings.

        **Fontes e APIs utilizadas:**

        - **Artificial Analysis** — [artificialanalysis.ai](https://artificialanalysis.ai) ·
          índice de qualidade proprietário, velocidade medida e preços de mercado.
          Endpoint: `GET /api/v2/data/llms/models` (autenticado).
        - **LMSYS Chatbot Arena** — [lmarena.ai](https://lmarena.ai) ·
          rankings Elo baseados em votos cegos de usuários. Dados públicos via Hugging Face.
        - **Hugging Face Hub** — [huggingface.co](https://huggingface.co) ·
          popularidade de modelos open-source (downloads e likes).
          Acesso via biblioteca `huggingface_hub`.

        **Atualização:** cache de 1 hora. Clique em "Atualizar dados" na barra lateral para forçar refresh.

        **Sobre {cfg.COMPANY_NAME}:** {cfg.COMPANY_TAGLINE}
        """
    )
    st.info(
        "Este dashboard foi construído para transparência. "
        "Os números mudam com frequência — se alguma informação parecer fora do esperado, "
        "provavelmente é reflexo de um release recente no mercado."
    )


# =========================================================================
# FOOTER — links de volta ao site
# =========================================================================
st.markdown(
    f"""
    <div class="mx-footer">
      <div class="left">
        © {datetime.now().year} <span class="brand"><span class="orange">Maximiz</span><span class="purple">IA</span></span> · Consultoria em IA
      </div>
      <div class="right">
        <a href="{cfg.COMPANY_SITE_URL}" target="_blank" class="link">maximizia.com.br</a>
        <a href="{cfg.COMPANY_LINKEDIN_URL}" target="_blank" class="link">LinkedIn</a>
        <a href="{cfg.COMPANY_WHATSAPP_URL}" target="_blank" class="link">WhatsApp</a>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
