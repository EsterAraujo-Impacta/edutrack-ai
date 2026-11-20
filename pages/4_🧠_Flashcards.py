"""pages/4_🧠_Flashcards.py – Revisão Espaçada (SM-2) e Gestão de Flashcards."""

from datetime import date, datetime
import streamlit as st
from pages.session_helper import (
    FLASHCARDS_API_BASE,
    load_user_flashcards,
    load_user_workspace,
    require_login,
    xano_request,
)
from scripts.spaced_repetition import calculate_sm2, preview_intervals

st.set_page_config(page_title="Flashcards – EduTrack AI", page_icon="🧠")
token = require_login()

user, subjects_list, _ = load_user_workspace(token)
user_id = user.get("id")
nome_aluno = user.get("nome") or "Estudante"

st.title("🧠 Flashcards (Repetição Espaçada)")
st.caption(
    f"Olá, **{nome_aluno}**! Revise seus cartões no momento ideal para fixar o"
    " conteúdo."
)

subject_map = {
    s["id"]: (s.get("name") or s.get("nome") or f"Disciplina #{s['id']}")
    for s in subjects_list
}

try:
  my_cards = load_user_flashcards(token, user_id)
except Exception as exc:
  st.error(f"Erro ao carregar flashcards do Xano: {exc}")
  st.stop()

today_str = date.today().strftime("%Y-%m-%d")

tab_estudar, tab_gerenciar = st.tabs(
    ["🎯 Estudar Agora", "🗂️ Criar e Gerenciar Cartões"]
)

# ---------------------------------------------------------------------------
# ABA 1: FILA DE REVISÃO (SM-2)
# ---------------------------------------------------------------------------
with tab_estudar:
  # Filtro por disciplina na fila de estudo
  opcoes_filtro = ["Todas"] + list(subject_map.keys())
  disc_selecionada = st.selectbox(
      "Filtrar fila de revisão por disciplina:",
      options=opcoes_filtro,
      format_func=lambda x: (
          "Todas as disciplinas" if x == "Todas" else subject_map[x]
      ),
  )

  # Busca apenas os cartões cuja ProximaRevisao <= hoje
  due_cards = []
  for card in my_cards:
    next_rev = str(card.get("next_review") or today_str)[:10]
    if next_rev <= today_str:
      if (
          disc_selecionada == "Todas"
          or card.get("subject_id") == disc_selecionada
      ):
        due_cards.append(card)

  due_cards.sort(key=lambda c: str(c.get("next_review") or today_str))

  if not due_cards:
    st.success(
        "🎉 **Parabéns! Você zerou sua fila de revisão por hoje!**\n\n"
        "Todos os cartões selecionados estão em dia. Volte amanhã ou crie"
        " novos flashcards na aba ao lado."
    )
  else:
    st.info(f"📌 Cartões pendentes para revisão hoje: **{len(due_cards)}**")

    current_card = due_cards[0]
    card_id = current_card["id"]
    subj_name = subject_map.get(
        current_card.get("subject_id"), "Geral / Sem disciplina"
    )

    reveal_key = f"reveal_card_{card_id}"
    if reveal_key not in st.session_state:
      st.session_state[reveal_key] = False

    # Card UI
    with st.container(border=True):
      st.caption(
          f"📚 **{subj_name}** • Repetições: {current_card.get('repetitions', 0)}"
          f" • Facilidade: {current_card.get('ease_factor', 2.5):.2f}"
      )
      st.markdown("### ❓ Pergunta (Frente)")
      st.markdown(f"#### {current_card.get('front', '')}")

      if not st.session_state[reveal_key]:
        st.write("")
        if st.button(
            "👁️ Mostrar Resposta",
            key=f"btn_show_{card_id}",
            type="primary",
            use_container_width=True,
        ):
          st.session_state[reveal_key] = True
          st.rerun()
      else:
        st.divider()
        st.markdown("### 💡 Resposta (Verso)")
        st.info(current_card.get("back", ""))

        st.write("**Como foi lembrar dessa resposta?**")

        previews = preview_intervals(
            interval=current_card.get("interval", 0),
            repetitions=current_card.get("repetitions", 0),
            ease_factor=current_card.get("ease_factor", 2.5),
        )

        def _submit_review(grade: int):
          updated_fields = calculate_sm2(
              interval=current_card.get("interval", 0),
              repetitions=current_card.get("repetitions", 0),
              ease_factor=current_card.get("ease_factor", 2.5),
              grade=grade,
          )
          payload = {
              "user_id": user_id,
              "subject_id": current_card.get("subject_id"),
              "front": current_card.get("front"),
              "back": current_card.get("back"),
              **updated_fields,
          }
          try:
            xano_request(
                FLASHCARDS_API_BASE,
                f"/flashcards/{card_id}",
                method="PATCH",
                data=payload,
                token_jwt=token,
            )
            st.session_state.pop(reveal_key, None)
            st.cache_data.clear()
            st.rerun()
          except Exception as err:
            st.error(f"Erro ao salvar revisão: {err}")

        c0, c1, c2, c3 = st.columns(4)
        with c0:
          if st.button(
              f"🔴 Errei (0)\n\n({previews[0]}d)",
              key=f"btn_g0_{card_id}",
              use_container_width=True,
          ):
            _submit_review(0)
        with c1:
          if st.button(
              f"🟠 Difícil (1)\n\n({previews[1]}d)",
              key=f"btn_g1_{card_id}",
              use_container_width=True,
          ):
            _submit_review(1)
        with c2:
          if st.button(
              f"🟢 Bom (2)\n\n({previews[2]}d)",
              key=f"btn_g2_{card_id}",
              use_container_width=True,
          ):
            _submit_review(2)
        with c3:
          if st.button(
              f"🔵 Fácil (3)\n\n({previews[3]}d)",
              key=f"btn_g3_{card_id}",
              use_container_width=True,
          ):
            _submit_review(3)

# ---------------------------------------------------------------------------
# ABA 2: CRIAR E GERENCIAR FLASHCARDS
# ---------------------------------------------------------------------------
with tab_gerenciar:
  st.subheader("➕ Novo Flashcard")
  with st.form("form_novo_flashcard", clear_on_submit=True):
    frente = st.text_area(
        "Frente (Pergunta ou Conceito) *",
        placeholder="Ex: Qual a diferença entre INNER JOIN e LEFT JOIN no SQL?",
    )
    verso = st.text_area(
        "Verso (Resposta) *",
        placeholder=(
            "Ex: INNER JOIN retorna apenas registros com correspondência nas"
            " duas tabelas; LEFT JOIN retorna todos da tabela à esquerda."
        ),
    )

    if subjects_list:
      disc_id = st.selectbox(
          "Disciplina vinculada *",
          options=list(subject_map.keys()),
          format_func=lambda x: subject_map[x],
      )
    else:
      disc_id = None
      st.caption(
          "Dica: Cadastre disciplinas na aba **Disciplinas** para organizar"
          " seus baralhos por matéria."
      )

    if st.form_submit_button("Salvar Flashcard"):
      if not frente.strip() or not verso.strip():
        st.warning("Preencha tanto a Frente quanto o Verso do cartão.")
      else:
        try:
          payload = {
              "user_id": user_id,
              "subject_id": disc_id,
              "front": frente.strip(),
              "back": verso.strip(),
              "interval": 0,
              "repetitions": 0,
              "ease_factor": 2.5,
              "next_review": today_str,
          }
          xano_request(
              FLASHCARDS_API_BASE,
              "/flashcards",
              method="POST",
              data=payload,
              token_jwt=token,
          )
          st.cache_data.clear()
          st.success("Flashcard adicionado à fila de revisão de hoje!")
          st.rerun()
        except Exception as exc:
          st.error(f"Erro ao criar flashcard: {exc}")

  st.divider()
  st.subheader(f"📚 Todos os Meus Flashcards ({len(my_cards)})")

  if not my_cards:
    st.info("Você ainda não criou nenhum flashcard.")
  else:
    for card in my_cards:
      cid = card["id"]
      s_name = subject_map.get(card.get("subject_id"), "Sem disciplina")
      raw_next = str(card.get("next_review") or today_str)[:10]
      try:
        fmt_next = datetime.strptime(raw_next, "%Y-%m-%d").strftime("%d/%m/%Y")
      except ValueError:
        fmt_next = raw_next

      status_badge = "🔥 Revisar hoje" if raw_next <= today_str else f"📅 {fmt_next}"

      with st.expander(f"[{s_name}] {card.get('front')} — ({status_badge})"):
        st.write(f"**Resposta:** {card.get('back')}")
        st.caption(
            f"Intervalo: {card.get('interval', 0)}d | Repetições:"
            f" {card.get('repetitions', 0)} | Fator:"
            f" {card.get('ease_factor', 2.5):.2f}"
        )
        if st.button("🗑️ Excluir Cartão", key=f"del_fc_{cid}"):
          try:
            xano_request(
                FLASHCARDS_API_BASE,
                f"/flashcards/{cid}",
                method="DELETE",
                token_jwt=token,
            )
            st.cache_data.clear()
            st.rerun()
          except Exception as exc:
            st.error(f"Erro ao excluir flashcard: {exc}")