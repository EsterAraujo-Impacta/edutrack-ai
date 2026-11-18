# Proposta: Migração de `.env` para Streamlit Secrets (`st.secrets`)

## Objetivo
Substituir a leitura de variáveis de ambiente via `python-dotenv` (`.env`) pela leitura nativa via `st.secrets` do Streamlit, mantendo compatibilidade para execução no Streamlit Community Cloud e em ambiente local.

## Alterações Planejadas
1. **`pages/auth_helper.py`**: Atualizar o carregamento da `XANO_API_BASE` para priorizar `st.secrets` com fallback para `os.getenv`.
2. **`pages/1_📚_Disciplinas.py`**: Atualizar a leitura de `XANO_SUBJECT_API_BASE`, `XANO_AUTH_API_BASE` e `XANO_ACADEMIC_API_BASE` para ler de `st.secrets` (com fallback para `os.getenv`).
3. **`scripts/generate_report.py`**: Garantir que a resolução das URLs base suporte `st.secrets` quando executado dentro do Streamlit e `os.getenv` quando executado via CLI.
4. **Limpeza**: Remover dependência obrigatória do arquivo `.env` na raiz do projeto.