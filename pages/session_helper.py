"""pages/session_helper.py – Gerenciador centralizado de sessão, temas, cache e sidebar."""

from datetime import datetime
import json
import os
import urllib.error
import urllib.request
import streamlit as st
from scripts.theme_manager import inject_theme_css, render_theme_switcher


def get_secret(key: str, default: str = "") -> str:
  try:
    if key in st.secrets:
      return str(st.secrets[key]).strip().rstrip("/")
  except Exception:
    pass
  return os.getenv(key, default).strip().rstrip("/")


AUTH_API_BASE = get_secret("XANO_AUTH_API_BASE") or get_secret("XANO_API_BASE")
SUBJECT_API_BASE = get_secret("XANO_SUBJECT_API_BASE") or AUTH_API_BASE
ACADEMIC_API_BASE = get_secret("XANO_ACADEMIC_API_BASE") or AUTH_API_BASE
FLASHCARDS_API_BASE = (
    get_secret("XANO_FLASHCARDS_API_BASE") or ACADEMIC_API_BASE
)
NOTES_API_BASE = get_secret("XANO_NOTES_API_BASE") or AUTH_API_BASE


def xano_request(
    base_url: str,
    endpoint: str,
    method: str = "GET",
    data: dict | None = None,
    token_jwt: str | None = None,
):
  url = f"{base_url}{endpoint}"
  headers = {"Content-Type": "application/json", "Accept": "application/json"}
  if token_jwt:
    headers["Authorization"] = f"Bearer {token_jwt}"

  encoded_data = json.dumps(data).encode("utf-8") if data is not None else None
  req = urllib.request.Request(
      url, data=encoded_data, headers=headers, method=method.upper()
  )

  try:
    with urllib.request.urlopen(req, timeout=15) as resp:
      raw = resp.read().decode(resp.headers.get_content_charset() or "utf-8")
      return json.loads(raw) if raw else None
  except urllib.error.HTTPError as exc:
    body = exc.read().decode("utf-8", errors="ignore")
    try:
      msg = json.loads(body).get("message", body)
    except Exception:
      msg = body
    raise RuntimeError(f"HTTP {exc.code}: {msg}") from None
  except urllib.error.URLError as exc:
    raise RuntimeError(f"Erro de conexão: {exc.reason}") from None


@st.cache_data(ttl=120, show_spinner=False)
def load_user_workspace(jwt: str):
  """Carrega usuário, disciplinas e tarefas com cache de 2 min para evitar HTTP 429."""
  user = xano_request(AUTH_API_BASE, "/auth/me", method="GET", token_jwt=jwt)
  user_id = user.get("id")

  subjects = (
      xano_request(
          SUBJECT_API_BASE, "/subjects", method="GET", token_jwt=jwt
      )
      or []
  )
  all_tasks = (
      xano_request(
          ACADEMIC_API_BASE, "/academic_tasks", method="GET", token_jwt=jwt
      )
      or []
  )

  my_subjects = [s for s in subjects if s.get("user_id") == user_id]
  my_tasks = [t for t in all_tasks if t.get("user_id") == user_id]

  return user, my_subjects, my_tasks


@st.cache_data(ttl=120, show_spinner=False)
def load_user_flashcards(jwt: str, user_id: int) -> list[dict]:
  """Carrega os flashcards do usuário logado com cache."""
  cards = (
      xano_request(
          FLASHCARDS_API_BASE, "/flashcards", method="GET", token_jwt=jwt
      )
      or []
  )
  return [c for c in cards if c.get("user_id") == user_id]


@st.cache_data(ttl=120, show_spinner=False)
def load_user_notes(jwt: str, user_id: int) -> list[dict]:
  """Busca todas as anotações do usuário logado."""
  try:
    notes = (
        xano_request(NOTES_API_BASE, "/notes", method="GET", token_jwt=jwt)
        or []
    )
    if isinstance(notes, dict):
      notes = [notes]
    return [n for n in notes if n.get("user_id") == user_id]
  except Exception:
    return []


def create_user_note(jwt: str, content: str) -> dict:
  """Cria uma nova anotação no Xano."""
  now_str = datetime.now().strftime("%d/%m/%Y às %H:%M")
  res = xano_request(
      NOTES_API_BASE,
      "/notes",
      method="POST",
      data={"content": content, "updated_at": now_str},
      token_jwt=jwt,
  )
  load_user_notes.clear()
  return res or {"content": content, "updated_at": now_str}


def update_user_note(jwt: str, note_id: int, content: str) -> dict:
  """Atualiza uma anotação existente (inclusive limpando o texto)."""
  now_str = datetime.now().strftime("%d/%m/%Y às %H:%M")
  res = xano_request(
      NOTES_API_BASE,
      f"/notes/{note_id}",
      method="PATCH",
      data={"content": content, "updated_at": now_str},
      token_jwt=jwt,
  )
  load_user_notes.clear()
  return res or {"id": note_id, "content": content, "updated_at": now_str}


def delete_user_note(jwt: str, note_id: int) -> None:
  """Exclui uma anotação."""
  xano_request(
      NOTES_API_BASE,
      f"/notes/{note_id}",
      method="DELETE",
      token_jwt=jwt,
  )
  load_user_notes.clear()


def render_sidebar_auth() -> str | None:
  """Injeta o tema global e renderiza seletor de temas, login, nota rápida e Sair."""
  inject_theme_css()
  token = st.session_state.get("jwt_token")

  with st.sidebar:
    st.divider()
    render_theme_switcher()
    st.divider()

    if token:
      try:
        user, _, _ = load_user_workspace(token)
      except Exception as exc:
        err_str = str(exc)
        if "401" in err_str or "403" in err_str:
          st.warning("Sessão expirada. Faça login novamente.")
          st.session_state.pop("jwt_token", None)
          st.cache_data.clear()
          return None
        else:
          st.warning(
              "⏳ Servidor ocupando limite de requisições. Aguarde 15s e"
              " recarregue."
          )
          return token

      nome = user.get("nome") or user.get("email") or "Estudante"
      st.success(f"👤 Conectado como:\n**{nome}**")

      # Mini Quick Notes na Sidebar
      with st.expander("🗒️ Anotação Rápida", expanded=False):
        with st.form("form_sidebar_quick_note", clear_on_submit=True):
          side_text = st.text_area(
              "Anotação rápida",
              height=110,
              label_visibility="collapsed",
              placeholder="Escreva um lembrete rápido...",
          )
          submitted_side = st.form_submit_button(
              "💾 Salvar anotação", use_container_width=True
          )

        if submitted_side:
          if side_text.strip():
            try:
              create_user_note(token, side_text.strip())
              st.toast("Anotação salva!", icon="✅")
              st.rerun()
            except Exception as exc:
              st.error(f"Erro ao salvar: {exc}")
          else:
            st.toast("Digite algo antes de salvar.", icon="⚠️")

      if st.button("🚪 Sair (Logout)", use_container_width=True):
        st.session_state.pop("jwt_token", None)
        st.cache_data.clear()
        st.rerun()
    else:
      st.info("🔒 Você não está logado.\nAcesse **Perfil** no menu acima.")

  return st.session_state.get("jwt_token")


def require_login() -> str:
  """Bloqueia a página se não houver login ativo na sessão."""
  token = render_sidebar_auth()
  if not token:
    st.warning(
        "🔒 **Acesso restrito:** Faça login na página **👤 Perfil** (no menu"
        " lateral) para visualizar e gerenciar seus dados."
    )
    st.stop()
  return token