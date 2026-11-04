"""pages/3_👤_Perfil.py – Página de cadastro, login e perfil do EduTrack AI.

Integração com os endpoints Xano de autenticação:
  - POST /auth/signup  → campos: email (email), senha (password), nome (text, opcional)
                         resposta: { authToken: "<jwt>" }
  - POST /auth/login   → campos: email (email), senha (text)
                         resposta: { authToken: "<jwt>" }
  - GET  /auth/me      → requer header Authorization: Bearer <token>
                         resposta: { id, created_at, nome, email }

Tabela `user` no Xano:
  - id          : int (PK)
  - created_at  : timestamp
  - nome        : text (opcional)
  - email       : email (opcional, lowercase + trim)
  - senha       : password (sensitive/internal)
"""

import streamlit as st
from pathlib import Path

from pages.auth_helper import post, get

# ---------------------------------------------------------------------------
# Helpers de token (session_state + arquivo .auth_token opcional)
# ---------------------------------------------------------------------------

def _save_token(token: str) -> None:
    """Persiste o JWT no session_state e, opcionalmente, em .auth_token."""
    st.session_state["jwt_token"] = token
    try:
        Path(".auth_token").write_text(token, encoding="utf-8")
    except Exception:
        pass  # Falha silenciosa — o arquivo .auth_token não é essencial para a UI


def _get_token() -> str | None:
    return st.session_state.get("jwt_token")


# ---------------------------------------------------------------------------
# Layout da página
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Perfil – EduTrack AI", page_icon="👤")
st.title("👤 Perfil do Usuário")

# ---------------------------------------------------------------------------
# Formulário de Cadastro — POST /auth/signup
# Campos: email, senha, nome (opcional)
# Resposta esperada: { authToken: "<jwt>" }
# ---------------------------------------------------------------------------

st.header("Criar nova conta")
with st.form(key="form_signup"):
    signup_email = st.text_input("E-mail *")
    signup_senha = st.text_input("Senha *", type="password")
    signup_nome = st.text_input("Nome (opcional)")
    submitted_signup = st.form_submit_button("Cadastrar")

if submitted_signup:
    if not signup_email or not signup_senha:
        st.error("E-mail e senha são obrigatórios para o cadastro.")
    else:
        # Payload usa os nomes de campo da tabela user: "email", "senha", "nome"
        payload: dict = {"email": signup_email, "senha": signup_senha}
        if signup_nome:
            payload["nome"] = signup_nome
        try:
            resp = post("/auth/signup", payload)
            # Xano retorna { authToken: "<jwt>" } no signup
            token = resp.get("authToken")
            if token:
                _save_token(token)
                st.success("Conta criada e login realizado com sucesso!")
                st.rerun()
            else:
                st.success("Conta criada com sucesso! Faça login abaixo.")
        except RuntimeError as exc:
            st.error(f"Falha no cadastro: {exc}")

st.divider()

# ---------------------------------------------------------------------------
# Formulário de Login — POST /auth/login
# Campos: email, senha
# Resposta esperada: { authToken: "<jwt>" }
# ---------------------------------------------------------------------------

st.header("Login")
with st.form(key="form_login"):
    login_email = st.text_input("E-mail *", key="login_email")
    login_senha = st.text_input("Senha *", type="password", key="login_senha")
    submitted_login = st.form_submit_button("Entrar")

if submitted_login:
    if not login_email or not login_senha:
        st.error("E-mail e senha são obrigatórios para o login.")
    else:
        try:
            resp = post("/auth/login", {"email": login_email, "senha": login_senha})
            # Xano retorna { authToken: "<jwt>" } no login
            token = resp.get("authToken")
            if not token:
                raise RuntimeError(
                    "Token não encontrado na resposta. "
                    "Verifique se o endpoint /auth/login retorna { authToken: ... }."
                )
            _save_token(token)
            st.success("Login efetuado com sucesso!")
            st.rerun()
        except RuntimeError as exc:
            st.error(f"Falha no login: {exc}")

st.divider()

# ---------------------------------------------------------------------------
# Perfil do usuário autenticado — GET /auth/me
# Requer: Authorization: Bearer <token>
# Resposta esperada: { id, created_at, nome, email }
# Renderizado apenas quando há token na sessão.
# ---------------------------------------------------------------------------

token = _get_token()
if token:
    st.header("Dados do usuário atual")
    try:
        user: dict = get("/auth/me", token=token)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("ID", user.get("id", "—"))
            st.text_input("Nome", value=user.get("nome") or "—", disabled=True)
        with col2:
            st.text_input("E-mail", value=user.get("email") or "—", disabled=True)
            st.text_input(
                "Conta criada em",
                value=str(user.get("created_at") or "—"),
                disabled=True,
            )

        if st.button("Sair"):
            st.session_state.pop("jwt_token", None)
            try:
                Path(".auth_token").unlink(missing_ok=True)
            except Exception:
                pass
            st.rerun()

    except RuntimeError as exc:
        st.error(f"Não foi possível carregar o perfil: {exc}")
        if "401" in str(exc) or "403" in str(exc):
            st.info("Seu token pode ter expirado. Faça login novamente.")
            st.session_state.pop("jwt_token", None)
else:
    st.info("Faça login para visualizar seus dados de perfil.")
