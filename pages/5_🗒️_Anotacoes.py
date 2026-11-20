"""pages/5_🗒️_Anotacoes.py – Bloco de Anotações Simples (Quick Notes) e Histórico."""

import streamlit as st
from pages.session_helper import (
    create_user_note,
    delete_user_note,
    load_user_notes,
    load_user_workspace,
    require_login,
    update_user_note,
)

st.set_page_config(page_title="Anotações – EduTrack AI", page_icon="🗒️")
token = require_login()

user, _, _ = load_user_workspace(token)
user_id = user.get("id")
nome_aluno = user.get("nome") or "Estudante"

st.title("🗒️ Bloco de Anotações Rápidas")
st.caption(
    f"Olá, **{nome_aluno}**! Escreva rascunhos em texto puro e acompanhe"
    " todas as suas anotações salvas."
)

# Carrega todas as anotações do usuário e ordena da mais recente para a mais antiga
all_notes = load_user_notes(token, user_id)
all_notes.sort(key=lambda n: n.get("id", 0), reverse=True)

# Estilização minimalista em texto puro (Plain Text)
st.markdown(
    """
    <style>
    textarea {
        font-family: 'Consolas', 'Courier New', monospace !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
        border-radius: 8px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 1. BLOCO DE RASCUNHO RÁPIDO (NOVA ANOTAÇÃO COM LIMPEZA AUTOMÁTICA)
# ---------------------------------------------------------------------------
st.subheader("✍️ Nova Anotação")

with st.form("form_nova_anotacao", clear_on_submit=True):
  texto_rascunho = st.text_area(
      label="Bloco de rascunho",
      height=200,
      label_visibility="collapsed",
      placeholder="Digite suas anotações, fórmulas ou lembretes em texto puro...",
  )
  submitted = st.form_submit_button("💾 Salvar Anotação", type="primary")

  if submitted:
    if not texto_rascunho.strip():
      st.warning("Escreva algum conteúdo antes de salvar.")
    else:
      try:
        create_user_note(token, texto_rascunho.strip())
        st.toast("Anotação salva na sua lista!", icon="✅")
        st.rerun()
      except Exception as exc:
        st.error(f"Erro ao salvar anotação: {exc}")

st.divider()

# ---------------------------------------------------------------------------
# 2. VISUALIZAÇÃO DAS ANOTAÇÕES FEITAS
# ---------------------------------------------------------------------------
st.subheader(f"📚 Minhas Anotações Salvas ({len(all_notes)})")

if not all_notes:
  st.info(
      "Você ainda não possui anotações salvas. Use o bloco acima para criar a"
      " primeira!"
  )
else:
  for note in all_notes:
    note_id = note["id"]
    content = note.get("content") or ""
    updated_at = note.get("updated_at") or "Data não registrada"

    first_line = (
        content.splitlines()[0] if content.strip() else "(Anotação vazia)"
    )
    preview_title = (
        first_line[:55] + "..." if len(first_line) > 55 else first_line
    )

    with st.expander(f"📝 {preview_title}  •  🕒 {updated_at}", expanded=False):
      edited_content = st.text_area(
          "Editar conteúdo",
          value=content,
          height=150,
          label_visibility="collapsed",
          key=f"edit_note_area_{note_id}",
      )

      c_upd, c_del, _ = st.columns([1.3, 1.3, 2.4])
      with c_upd:
        if st.button(
            "💾 Atualizar",
            key=f"btn_upd_note_{note_id}",
            use_container_width=True,
        ):
          try:
            update_user_note(token, note_id, edited_content)
            st.toast("Anotação atualizada!", icon="✅")
            st.rerun()
          except Exception as exc:
            st.error(f"Erro ao atualizar: {exc}")

      with c_del:
        if st.button(
            "🗑️ Excluir",
            key=f"btn_del_note_{note_id}",
            use_container_width=True,
        ):
          try:
            delete_user_note(token, note_id)
            st.toast("Anotação excluída!", icon="🗑️")
            st.rerun()
          except Exception as exc:
            st.error(f"Erro ao excluir: {exc}")