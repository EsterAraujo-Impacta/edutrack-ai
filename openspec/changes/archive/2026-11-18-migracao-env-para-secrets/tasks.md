# Tasks: Migração de Variáveis de Ambiente para Secrets do Streamlit

## 1. Helper de Configuração
- [x] 1.1 Atualizar `pages/auth_helper.py` para incluir a função utilitária `get_config(key, default)` priorizando `st.secrets` com fallback para `os.getenv`
- [x] 1.2 Atualizar a inicialização de `XANO_API_BASE` em `pages/auth_helper.py` para usar `get_config`

## 2. Atualização das Páginas do Streamlit
- [x] 2.1 Atualizar `pages/1_📚_Disciplinas.py` para obter `XANO_SUBJECT_API_BASE`, `XANO_AUTH_API_BASE` e `XANO_ACADEMIC_API_BASE` através de `get_config`
- [x] 2.2 Atualizar `pages/3_👤_Perfil.py` para obter as URLs via `get_config`
- [x] 2.3 Atualizar `services/subjects_service.py` para suportar `get_config` ou `st.secrets`

## 3. Scripts e Segurança
- [x] 3.1 Atualizar `scripts/generate_report.py` para tentar `st.secrets` quando executado no contexto Streamlit
- [x] 3.2 Verificar `.gitignore` para assegurar que `.streamlit/` e `.env` estão devidamente protegidos
