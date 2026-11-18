"""pages/session_helper.py – Gerenciador centralizado de sessão, cache e sidebar."""

import json
import os
import urllib.error
import urllib.request
import streamlit as st


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


@st.cache_data(ttl=45, show_spinner=False)
def load_user_workspace(jwt: str):
  """Carrega usuário, disciplinas e tarefas com cache de 45s para evitar HTTP 429."""
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

  # Garante isolamento estrito por user_id
  my_subjects = [s for s in subjects if s.get("user_id") == user_id]
  my_tasks = [t for t in all_tasks if t.get("user_id") == user_id]

  return user, my_subjects, my_tasks


def render_sidebar_auth() -> str | None:
  """Renderiza status de login e botão Sair na barra lateral. Retorna o token ativo."""
  token = st.session_state.get("jwt_token")

  with st.sidebar:
    st.divider()
    if token:
      try:
        user, _, _ = load_user_workspace(token)
        nome = user.get("nome") or user.get("email") or "Estudante"
        st.success(f"👤 Conectado como:\n**{nome}**")
        if st.button("🚪 Sair (Logout)", use_container_width=True):
          st.session_state.pop("jwt_token", None)
          st.cache_data.clear()
          st.rerun()
      except Exception:
        st.warning("Sessão expirada.")
        st.session_state.pop("jwt_token", None)
        st.cache_data.clear()
        return None
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