from datetime import date
import streamlit as st
from pages.session_helper import (
    load_user_flashcards,
    load_user_workspace,
    render_sidebar_auth,
)

st.set_page_config(page_title="EduTrack AI – Dashboard", page_icon="🎓")
st.title("🎓 EduTrack AI")
st.caption("Seu assistente inteligente de organização e desempenho acadêmico.")

token = render_sidebar_auth()

st.divider()

if not token:
  st.info(
      "👋 Bem-vindo ao **EduTrack AI**! Para acessar suas disciplinas, gerenciar"
      " tarefas, revisar flashcards e emitir relatórios em PDF, acesse a aba"
      " **👤 Perfil** no menu lateral esquerdo e entre com sua conta."
  )
else:
  try:
    user, subjects, tasks = load_user_workspace(token)
    user_id = user.get("id")
    nome = user.get("nome") or "Estudante"

    try:
      cards = load_user_flashcards(token, user_id)
      today_str = date.today().strftime("%Y-%m-%d")
      due_cards_count = sum(
          1
          for c in cards
          if str(c.get("next_review") or today_str)[:10] <= today_str
      )
    except Exception:
      due_cards_count = 0

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

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📚 Disciplinas", total_disc)
    col2.metric("⏳ Tarefas Pendentes", pendentes)
    col3.metric("✅ Concluídas", concluidas)
    col4.metric("🧠 Flashcards Hoje", due_cards_count)

    if total_tasks > 0:
      st.write("")
      pct = concluidas / total_tasks
      st.progress(pct, text=f"Progresso geral das atividades: {pct * 100:.0f}%")

  except Exception as e:
    st.error(f"Erro ao carregar seu resumo: {e}")
    if st.button("🔄 Recarregar dados"):
      st.cache_data.clear()
      st.rerun()