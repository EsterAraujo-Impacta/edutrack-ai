from datetime import date, datetime
import time
import streamlit as st
from pages.session_helper import (
    ACADEMIC_API_BASE,
    load_user_workspace,
    require_login,
    xano_request,
)

st.set_page_config(page_title="Minhas Tarefas", page_icon="📝")
token = require_login()

user_data, subjects_list, my_tasks = load_user_workspace(token)
user_id = user_data.get("id")
nome_aluno = user_data.get("nome") or "Estudante"

st.title("📝 Minhas Tarefas")
st.caption(f"Olá, **{nome_aluno}**! Acompanhe suas entregas e prazos.")

subject_map = {
    s["id"]: (s.get("name") or s.get("nome") or f"Disciplina #{s['id']}")
    for s in subjects_list
}

# Barra de Progresso Geral em Tempo Real
total_tasks = len(my_tasks)
completed_tasks = sum(
    1
    for t in my_tasks
    if str(t.get("status", "")).lower()
    in {"completed", "concluida", "concluída", "done"}
)
progress_pct = (completed_tasks / total_tasks) if total_tasks > 0 else 0.0

st.subheader("📊 Progresso Geral")
st.progress(
    progress_pct,
    text=(
        f"{completed_tasks} de {total_tasks} tarefas concluídas"
        f" ({progress_pct * 100:.0f}%)"
    ),
)

st.divider()

# Formulário de Nova Tarefa
with st.expander("➕ Nova Tarefa", expanded=False):
  if not subjects_list:
    st.info(
        "Cadastre pelo menos uma disciplina na aba **Disciplinas** antes de"
        " criar tarefas."
    )
  else:
    with st.form("form_nova_tarefa", clear_on_submit=True):
      titulo = st.text_input(
          "Título da Tarefa *", placeholder="Ex: Lista de Exercícios 01"
      )
      descricao = st.text_area(
          "Descrição (opcional)", placeholder="Detalhes, links ou observações..."
      )

      col_f1, col_f2 = st.columns(2)
      with col_f1:
        disciplina_id = st.selectbox(
            "Disciplina *",
            options=list(subject_map.keys()),
            format_func=lambda x: subject_map[x],
        )
      with col_f2:
        prazo = st.date_input("Data de Entrega *", value=date.today())

      submitted = st.form_submit_button("Salvar Tarefa")

      if submitted:
        if not titulo.strip():
          st.warning("Informe o título da tarefa.")
        else:
          try:
            payload = {
                "user_id": user_id,
                "subject_id": disciplina_id,
                "title": titulo.strip(),
                "description": descricao.strip(),
                "due_date": prazo.strftime("%Y-%m-%d"),
                "status": "pending",
                "created_at": int(time.time() * 1000),
            }
            xano_request(
                ACADEMIC_API_BASE,
                "/academic_tasks",
                method="POST",
                data=payload,
                token_jwt=token,
            )
            st.cache_data.clear()
            st.success(f"Tarefa **{titulo}** adicionada!")
            st.rerun()
          except Exception as exc:
            st.error(f"Erro ao salvar tarefa: {exc}")

# Filtros
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
  search = st.text_input("🔍 Buscar tarefa...", placeholder="Ex: Estudar Pandas")
with col2:
  opcoes_disc = ["Todas"] + list(subject_map.keys())
  filtro_disc = st.selectbox(
      "Disciplina",
      options=opcoes_disc,
      format_func=lambda x: "Todas" if x == "Todas" else subject_map[x],
  )
with col3:
  filtro_status = st.selectbox("Status", ["Todas", "Pendentes", "Concluídas"])

filtered_tasks = []
for t in my_tasks:
  is_done = str(t.get("status", "")).lower() in {
      "completed",
      "concluida",
      "concluída",
      "done",
  }
  if filtro_status == "Pendentes" and is_done:
    continue
  if filtro_status == "Concluídas" and not is_done:
    continue
  if filtro_disc != "Todas" and t.get("subject_id") != filtro_disc:
    continue
  if search.strip() and search.strip().lower() not in t.get("title", "").lower():
    continue
  filtered_tasks.append(t)

filtered_tasks.sort(key=lambda x: str(x.get("due_date") or "9999-12-31"))

st.markdown("---")

if not filtered_tasks:
  st.info("Nenhuma tarefa encontrada para os filtros selecionados.")
else:
  for task in filtered_tasks:
    task_id = task["id"]
    is_done = str(task.get("status", "")).lower() in {
        "completed",
        "concluida",
        "concluída",
        "done",
    }
    subj_name = subject_map.get(
        task.get("subject_id"), "Disciplina não vinculada"
    )

    raw_date = str(task.get("due_date") or "")
    try:
      fmt_date = datetime.strptime(raw_date[:10], "%Y-%m-%d").strftime(
          "%d/%m/%Y"
      )
    except ValueError:
      fmt_date = raw_date or "Sem prazo"

    icon = "✅" if is_done else "⏳"
    header_label = f"{icon} {task.get('title')} — *{subj_name}* (Prazo: {fmt_date})"

    with st.expander(header_label, expanded=not is_done):
      if task.get("description"):
        st.write(task["description"])

      c_check, c_del = st.columns([4, 1])

      with c_check:
        checked = st.checkbox(
            "Marcar como Concluída",
            value=is_done,
            key=f"chk_task_{task_id}",
        )
        if checked != is_done:
          new_status = "completed" if checked else "pending"
          try:
            payload_update = dict(task)
            payload_update["status"] = new_status
            payload_update.pop("id", None)

            xano_request(
                ACADEMIC_API_BASE,
                f"/academic_tasks/{task_id}",
                method="PATCH",
                data=payload_update,
                token_jwt=token,
            )
            st.cache_data.clear()
            st.rerun()
          except Exception as exc:
            st.error(f"Erro ao atualizar status: {exc}")

      with c_del:
        if st.button("🗑️ Excluir", key=f"del_task_{task_id}", type="secondary"):
          try:
            xano_request(
                ACADEMIC_API_BASE,
                f"/academic_tasks/{task_id}",
                method="DELETE",
                token_jwt=token,
            )
            st.cache_data.clear()
            st.rerun()
          except Exception as exc:
            st.error(f"Erro ao excluir tarefa: {exc}")