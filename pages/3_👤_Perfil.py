import io
import streamlit as st
from pages.auth_helper import get, post
from pages.session_helper import (
    AUTH_API_BASE,
    load_user_workspace,
    render_sidebar_auth,
)

st.set_page_config(page_title="Perfil – EduTrack AI", page_icon="👤")
st.title("👤 Perfil do Usuário")

token = render_sidebar_auth()


def _generate_report_pdf_bytes(jwt: str) -> bytes:
  from scripts.generate_report import fetch_report_data, generate_pdf_report

  data = fetch_report_data(api_base=AUTH_API_BASE, token=jwt)
  buffer = io.BytesIO()
  generate_pdf_report(report_data=data, output_path=buffer)
  buffer.seek(0)
  return buffer.getvalue()


if not token:
  tab_login, tab_signup = st.tabs(["🔑 Entrar", "📝 Criar Conta"])

  with tab_login:
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
          new_token = resp.get("authToken")
          if not new_token:
            raise RuntimeError("Token não retornado pela API.")
          st.cache_data.clear()
          st.session_state["jwt_token"] = new_token
          st.success("Login efetuado com sucesso!")
          st.rerun()
        except RuntimeError as exc:
          st.error(f"Falha no login: {exc}")

  with tab_signup:
    with st.form(key="form_signup"):
      signup_email = st.text_input("E-mail *")
      signup_senha = st.text_input("Senha *", type="password")
      signup_nome = st.text_input("Nome (opcional)")
      submitted_signup = st.form_submit_button("Cadastrar")

    if submitted_signup:
      if not signup_email or not signup_senha:
        st.error("E-mail e senha são obrigatórios para o cadastro.")
      else:
        payload = {"email": signup_email, "senha": signup_senha}
        if signup_nome:
          payload["nome"] = signup_nome
        try:
          resp = post("/auth/signup", payload)
          new_token = resp.get("authToken")
          if new_token:
            st.cache_data.clear()
            st.session_state["jwt_token"] = new_token
            st.success("Conta criada e login realizado com sucesso!")
            st.rerun()
          else:
            st.success("Conta criada! Faça login na aba ao lado.")
        except RuntimeError as exc:
          st.error(f"Falha no cadastro: {exc}")

else:
  try:
    user, my_subjects, my_tasks = load_user_workspace(token)
    st.subheader(f"Dados da Conta — {user.get('nome') or 'Estudante'}")

    col1, col2 = st.columns(2)
    with col1:
      st.text_input("Nome", value=user.get("nome") or "—", disabled=True)
      st.text_input("ID do Aluno", value=str(user.get("id", "—")), disabled=True)
    with col2:
      st.text_input("E-mail", value=user.get("email") or "—", disabled=True)
      st.text_input(
          "Conta criada em",
          value=str(user.get("created_at") or "—"),
          disabled=True,
      )

    st.divider()
    st.subheader("📄 Relatório de Desempenho Acadêmico")
    st.write(
        "Gere um documento PDF consolidado com todas as suas disciplinas e"
        " porcentagens de conclusão."
    )

    if st.button("⚙️ Preparar Relatório PDF"):
      with st.spinner("Gerando PDF..."):
        try:
          from scripts.generate_report import generate_pdf_report

          report_data = {
              "user": user,
              "subjects": my_subjects,
              "tasks": my_tasks,
          }
          buffer = io.BytesIO()
          generate_pdf_report(report_data=report_data, output_path=buffer)
          buffer.seek(0)

          st.download_button(
              label="📥 Baixar relatorio_desempenho.pdf",
              data=buffer.getvalue(),
              file_name="relatorio_desempenho.pdf",
              mime="application/pdf",
          )
        except Exception as report_err:
          st.error(f"Erro ao gerar PDF: {report_err}")
  except Exception as workspace_err:
    st.error(f"Erro ao carregar os dados da conta: {workspace_err}")