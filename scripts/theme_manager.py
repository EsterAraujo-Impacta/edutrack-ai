"""scripts/theme_manager.py – Provider de temas, persistência e componente Switcher."""

import streamlit as st
from scripts.themes import DEFAULT_THEME_KEY, THEMES, ThemeTokens


def get_active_theme_key() -> str:
  """Recupera o tema atual do estado da sessão ou dos query_params (persistência)."""
  if "app_theme" not in st.session_state:
    saved_param = st.query_params.get("theme", DEFAULT_THEME_KEY)
    if isinstance(saved_param, list):
      saved_param = saved_param[0] if saved_param else DEFAULT_THEME_KEY
    st.session_state["app_theme"] = (
        saved_param if saved_param in THEMES else DEFAULT_THEME_KEY
    )
  return st.session_state["app_theme"]


def get_active_theme() -> ThemeTokens:
  """Retorna o objeto ThemeTokens do tema ativo."""
  return THEMES[get_active_theme_key()]


def set_theme(theme_key: str) -> None:
  """Altera o tema ativo e persiste na URL (query_params) para sobreviver ao F5."""
  if theme_key in THEMES:
    st.session_state["app_theme"] = theme_key
    st.query_params["theme"] = theme_key


def inject_theme_css() -> ThemeTokens:
  """Injeta as variáveis CSS globais (Design Tokens) e garante contraste total."""
  theme = get_active_theme()
  scheme = "dark" if theme.is_dark else "light"
  bg_size = "140px 140px" if theme.bg_pattern != "none" else "auto"

  css = f"""
  <style>
  :root {{
      color-scheme: {scheme};
      --bg-primary: {theme.bg_primary};
      --surface: {theme.surface};
      --sidebar-bg: {theme.sidebar_bg};
      --text-primary: {theme.text_primary};
      --text-secondary: {theme.text_secondary};
      --border-color: {theme.border_color};
      --accent-color: {theme.accent_color};
      --accent-hover: {theme.accent_hover};
      --accent-text: {theme.accent_text};
  }}

  /* Fundo principal com padrão temático visível */
  .stApp {{
      background-color: var(--bg-primary) !important;
      background-image: {theme.bg_pattern} !important;
      background-repeat: repeat !important;
      background-size: {bg_size} !important;
      color: var(--text-primary) !important;
  }}

  /* Sidebar e cabeçalho */
  [data-testid="stSidebar"] {{
      background-color: var(--sidebar-bg) !important;
      border-right: 1px solid var(--border-color) !important;
  }}

  [data-testid="stHeader"] {{
      background-color: transparent !important;
  }}

  /* Garante contraste de texto em TODOS os elementos da página e sidebar */
  .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
  .stApp p, .stApp span, .stApp label, .stApp li, .stApp div,
  [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {{
      color: var(--text-primary);
  }}

  .stApp [data-testid="stCaptionContainer"] p,
  [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
      color: var(--text-secondary) !important;
  }}

  /* Containers brancos / superfícies (Expanders, Forms, Alertas, Métricas, Tabs) */
  [data-testid="stExpander"],
  [data-testid="stExpander"] details,
  [data-testid="stExpander"] summary,
  [data-testid="stForm"],
  [data-testid="stAlert"],
  [data-testid="stMetric"],
  [data-testid="stVerticalBlockBorderWrapper"] {{
      background-color: var(--surface) !important;
      color: var(--text-primary) !important;
      border-color: var(--border-color) !important;
  }}

  /* Inputs, Caixas de Texto e Selectbox (corrige texto branco no fundo branco) */
  div[data-baseweb="select"] > div,
  div[data-baseweb="input"] > div,
  div[data-baseweb="textarea"] > div,
  textarea,
  input {{
      background-color: var(--surface) !important;
      color: var(--text-primary) !important;
      -webkit-text-fill-color: var(--text-primary) !important;
      border-color: var(--border-color) !important;
  }}

  /* Dropdown / Lista de opções aberta do Selectbox */
  div[data-baseweb="popover"],
  ul[role="listbox"],
  ul[role="listbox"] li {{
      background-color: var(--surface) !important;
      color: var(--text-primary) !important;
  }}

  ul[role="listbox"] li:hover {{
      background-color: var(--sidebar-bg) !important;
  }}

  /* Botões Primários */
  .stButton > button[kind="primary"],
  .stFormSubmitButton > button[kind="primary"] {{
      background-color: var(--accent-color) !important;
      color: var(--accent-text) !important;
      border: none !important;
      font-weight: 600 !important;
  }}

  .stButton > button[kind="primary"] p,
  .stFormSubmitButton > button[kind="primary"] p {{
      color: var(--accent-text) !important;
  }}

  .stButton > button[kind="primary"]:hover,
  .stFormSubmitButton > button[kind="primary"]:hover {{
      background-color: var(--accent-hover) !important;
  }}

  /* Botões Secundários */
  .stButton > button:not([kind="primary"]),
  .stFormSubmitButton > button:not([kind="primary"]) {{
      background-color: var(--surface) !important;
      color: var(--text-primary) !important;
      border: 1px solid var(--border-color) !important;
  }}

  .stButton > button:not([kind="primary"]) p,
  .stFormSubmitButton > button:not([kind="primary"]) p {{
      color: var(--text-primary) !important;
  }}

  .stButton > button:not([kind="primary"]):hover,
  .stFormSubmitButton > button:not([kind="primary"]):hover {{
      border-color: var(--accent-color) !important;
  }}

  /* Troca visualmente o texto "app" no menu lateral por "🎓 Início" */
  [data-testid="stSidebarNavItems"] li:first-child a span {{
      display: none !important;
  }}
  [data-testid="stSidebarNavItems"] li:first-child a::after {{
      content: "🎓 Início";
      font-size: 14px;
      font-weight: 500;
      color: var(--text-primary);
  }}

  /* Esconde auth_helper e session_helper do menu lateral sem mover os arquivos */
  [data-testid="stSidebarNavItems"] li:has(a[href*="auth_helper"]),
  [data-testid="stSidebarNavItems"] li:has(a[href*="session_helper"]) {{
      display: none !important;
  }}
  </style>
  """
  st.markdown(css, unsafe_allow_html=True)
  return theme


def render_theme_switcher() -> None:
  """Renderiza apenas o seletor de temas na sidebar."""
  current_theme = get_active_theme()
  theme_keys = list(THEMES.keys())

  selected_key = st.selectbox(
      "🎨 Escolher tema",
      options=theme_keys,
      index=theme_keys.index(current_theme.key),
      format_func=lambda k: THEMES[k].label,
      key="select_app_theme",
  )

  if selected_key != current_theme.key:
    set_theme(selected_key)
    st.rerun()