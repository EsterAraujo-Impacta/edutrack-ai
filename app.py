import streamlit as st
from pages.session_helper import load_user_workspace, render_sidebar_auth

st.set_page_config(page_title="EduTrack AI – Dashboard", page_icon="🎓")
st.title("🎓 EduTrack AI")
st.caption("Seu assistente inteligente de organização e desempenho acadêmico.")

token = render_sidebar_auth()

st.divider()

if not token:
  st.info(
      "👋 Bem-vindo ao **EduTrack AI**! Para acessar suas disciplinas, gerenciar"
      " tarefas e emitir relatórios em PDF, acesse a aba **👤 Perfil** no menu"
      " lateral esquerdo e entre com sua conta."
  )
else:
  try:
    user, subjects, tasks = load_user_workspace(token)
    nome = user.get("nome") or "Estudante"

    st.subheader(f"Olá, {nome}! 👋")
    st.write("Aqui está o resumo atual do seu semestre:")

    total_disc = len(subjects)
    total_tasks = len(tasks)
    concluidas = sum(
        1
        for t in tasks
        if str(t.get("status", "")).lower()
        in {"completed", "concluida", "concluída", "done"}
    )
    pendentes = total_tasks - concluidas

    col1, col2, col3 = st.columns(3)
    col1.metric("📚 Disciplinas Ativas", total_disc)
    col2.metric("⏳ Tarefas Pendentes", pendentes)
    col3.metric("✅ Tarefas Concluídas", concluidas)

    if total_tasks > 0:
      st.write("")
      pct = concluidas / total_tasks
      st.progress(pct, text=f"Progresso geral das atividades: {pct * 100:.0f}%")

  except Exception as e:
    st.error(f"Erro ao carregar seu resumo: {e}")
    if st.button("🔄 Recarregar dados"):
      st.cache_data.clear()
      st.rerun()