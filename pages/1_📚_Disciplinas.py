import io
import os
import time
import json
import urllib.request
from datetime import datetime
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Disciplinas", page_icon="📚")

st.title("Gestão de Disciplinas")

# ---------------------------------------------------------------------------
# Identificação do Token e das URLs Base do Xano
# ---------------------------------------------------------------------------
token = st.session_state.get("jwt_token")
if not token:
    token_file = Path(".auth_token")
    if token_file.exists():
        token = token_file.read_text(encoding="utf-8").strip()

# Obtém as URLs bases do .env
subject_api_base = os.getenv("XANO_SUBJECT_API_BASE", "").rstrip("/")
auth_api_base = os.getenv("XANO_AUTH_API_BASE", "").rstrip("/")
academic_api_base = os.getenv("XANO_ACADEMIC_API_BASE", "").rstrip("/")

def xano_request(base_url: str, endpoint: str, method: str = "GET", data: dict = None, token_jwt: str = None) -> dict:
    """Função auxiliar para fazer requisições HTTP seguras apontando para o grupo de API correto."""
    url = f"{base_url.rstrip('/')}{endpoint}"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token_jwt:
        headers["Authorization"] = f"Bearer {token_jwt}"

    encoded_data = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method.upper())
    
    with urllib.request.urlopen(req, timeout=15) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return json.loads(resp.read().decode(charset))

# ---------------------------------------------------------------------------
# Botão de Download do Relatório de Desempenho (PDF)
# ---------------------------------------------------------------------------
if token:
    try:
        from scripts.generate_report import fetch_report_data, generate_pdf_report

        api_base = subject_api_base or os.getenv("XANO_API_BASE", "").rstrip("/")
        report_data = fetch_report_data(api_base=api_base, token=token)

        pdf_buffer = io.BytesIO()
        generate_pdf_report(report_data=report_data, output_path=pdf_buffer)
        pdf_buffer.seek(0)

        st.download_button(
            label="📄 Baixar Relatório de Desempenho (PDF)",
            data=pdf_buffer.getvalue(),
            file_name="relatorio_desempenho.pdf",
            mime="application/pdf",
            help="Clique para baixar o relatório completo com seu progresso nas disciplinas.",
        )
    except Exception as e:
        st.warning(f"Relatório PDF temporariamente indisponível: {e}")
else:
    st.info("💡 Faça login na aba **Perfil** para liberar a emissão do seu relatório PDF de desempenho.")

st.divider()

# Abas para separar Listagem de Cadastro
tab_lista, tab_novo = st.tabs(["📋 Listar", "➕ Nova Disciplina"])

with tab_novo:
    st.subheader("Cadastrar Nova Matéria")
    with st.form("form_disciplina"):
        nome = st.text_input("Nome da Disciplina", placeholder="ex: Python Basics")
        professor = st.text_input("Nome do Professor", placeholder="ex: Prof. Oriel")
        carga_horaria = st.number_input("Carga Horária (horas)", min_value=1, max_value=200, value=40)
        
        submitted = st.form_submit_button("Salvar")

        if submitted:
            if not token:
                st.error("Você precisa estar autenticado para cadastrar uma disciplina.")
            elif not nome or not professor:
                st.warning("Preencha o nome da disciplina e o professor.")
            else:
                try:
                    # 1. Busca os dados do usuário para obter o user_id ($auth.id)
                    user_data = xano_request(auth_api_base, "/auth/me", method="GET", token_jwt=token)
                    user_id = user_data.get("id")

                    # 2. Monta o payload exato para o Xano
                    payload = {
                        "name": nome,
                        "teacher": professor,
                        "hours": int(carga_horaria),
                        "user_id": user_id,
                        "created_at": int(time.time() * 1000)
                    }

                    # 3. Envia POST diretamente para o grupo de API de subjects (6HS-JuTA)
                    xano_request(subject_api_base, "/subjects", method="POST", data=payload, token_jwt=token)

                    st.success(f"Disciplina **{nome}** cadastrada com sucesso no Xano!")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Erro ao salvar no Xano: {exc}")

with tab_lista:
    if not token:
        st.info("Faça login para carregar suas disciplinas salvas no Xano.")
    else:
        try:
            # Busca as disciplinas reais diretamente no grupo de API de subjects (6HS-JuTA)
            subjects_data = xano_request(subject_api_base, "/subjects", method="GET", token_jwt=token)

            if not subjects_data:
                st.info("Nenhuma disciplina cadastrada no momento.")
            else:
                tabela_formatada = []
                for s in subjects_data:
                    tabela_formatada.append({
                        "ID": s.get("id"),
                        "Nome": s.get("name") or s.get("nome") or "—",
                        "Professor": s.get("teacher") or s.get("professor") or "—",
                        "Carga Horária": f"{s.get('hours')}h" if s.get("hours") is not None else "—"
                    })

                st.dataframe(tabela_formatada, use_container_width=True)
        except Exception as exc:
            st.error(f"Erro ao buscar disciplinas no Xano: {exc}")