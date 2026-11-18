import io
import time
import streamlit as st
from pages.session_helper import (
    SUBJECT_API_BASE,
    load_user_workspace,
    require_login,
    xano_request,
)

st.set_page_config(page_title="Disciplinas", page_icon="📚")
token = require_login()

user, subjects_data, tasks_data = load_user_workspace(token)
user_id = user.get("id")
nome_aluno = user.get("nome") or "Estudante"

st.title("📚 Gestão de Disciplinas")
st.caption(f"Olá, **{nome_aluno}**! Gerencie suas matérias cadastradas.")

# Botão sob demanda para gerar o PDF sem gastar requisições ao abrir a página
if st.button("📄 Gerar Relatório de Desempenho (PDF)"):
  with st.spinner("Montando PDF..."):
    try:
      from scripts.generate_report import generate_pdf_report

      report_data = {
          "user": user,
          "subjects": subjects_data,
          "tasks": tasks_data,
      }
      pdf_buffer = io.BytesIO()
      generate_pdf_report(report_data=report_data, output_path=pdf_buffer)
      pdf_buffer.seek(0)

      st.download_button(
          label="📥 Clique aqui para baixar o PDF",
          data=pdf_buffer.getvalue(),
          file_name="relatorio_desempenho.pdf",
          mime="application/pdf",
      )
    except Exception as e:
      st.error(f"Erro ao gerar PDF: {e}")

st.divider()

tab_lista, tab_novo = st.tabs(["📋 Minhas Disciplinas", "➕ Nova Disciplina"])

with tab_novo:
  st.subheader("Cadastrar Nova Matéria")
  with st.form("form_disciplina", clear_on_submit=True):
    nome = st.text_input("Nome da Disciplina *", placeholder="ex: Python Basics")
    professor = st.text_input(
        "Nome do Professor *", placeholder="ex: Prof. Oriel"
    )
    carga_horaria = st.number_input(
        "Carga Horária (horas)", min_value=1, max_value=300, value=40
    )

    submitted = st.form_submit_button("Salvar Disciplina")

    if submitted:
      if not nome.strip() or not professor.strip():
        st.warning("Preencha o nome da disciplina e o professor.")
      else:
        try:
          payload = {
              "name": nome.strip(),
              "teacher": professor.strip(),
              "hours": int(carga_horaria),
              "user_id": user_id,
              "created_at": int(time.time() * 1000),
          }
          xano_request(
              SUBJECT_API_BASE,
              "/subjects",
              method="POST",
              data=payload,
              token_jwt=token,
          )
          st.cache_data.clear()
          st.success(f"Disciplina **{nome}** cadastrada com sucesso!")
          st.rerun()
        except Exception as exc:
          st.error(f"Erro ao salvar no Xano: {exc}")

with tab_lista:
  if not subjects_data:
    st.info("Você ainda não possui disciplinas cadastradas.")
  else:
    tabela_formatada = [
        {
            "Nome": s.get("name") or s.get("nome") or "—",
            "Professor": s.get("teacher") or s.get("professor") or "—",
            "Carga Horária": (
                f"{s.get('hours')}h" if s.get("hours") is not None else "—"
            ),
        }
        for s in subjects_data
    ]
    st.dataframe(tabela_formatada, use_container_width=True)