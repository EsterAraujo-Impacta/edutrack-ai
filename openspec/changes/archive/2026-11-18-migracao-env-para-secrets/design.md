# Design: Migração para Streamlit Secrets

## Context

Atualmente o EduTrack AI carrega configurações sensíveis (URLs de API do Xano) de variáveis de ambiente (`os.getenv`) carregadas a partir de arquivos `.env` via `python-dotenv`. O Streamlit provê nativamente o dicionário `st.secrets`, carregado a partir de `.streamlit/secrets.toml` ou de variáveis injetadas na nuvem (Streamlit Community Cloud).

## Goals / Non-Goals

**Goals:**
- Centralizar o acesso a variáveis de configuração através de uma função helper unificada (`get_secret` / `get_config`), que tenta primeiro `st.secrets[key]`, depois `os.getenv(key)` e por fim um valor default.
- Atualizar `pages/auth_helper.py`, `pages/1_📚_Disciplinas.py`, `pages/3_👤_Perfil.py` e `services/subjects_service.py` para usar a nova abordagem.
- Manter o script standalone (`scripts/generate_report.py`, `scripts/calculate_progress.py`) funcional com fallback para `os.getenv`.
- Assegurar que `.streamlit/` continue ignorado no `.gitignore`.

**Non-Goals:**
- Deletar arquivos `.env` existentes dos desenvolvedores locais (apenas remover a obrigatoriedade estrita de depender de `.env` para o Streamlit rodar).

## Decisions

### 1. Função helper de configuração unificada
Criar a função helper `get_config(key: str, default: str = "") -> str` em `pages/auth_helper.py` (ou módulo de configuração):
```python
def get_config(key: str, default: str = "") -> str:
    try:
        import streamlit as st
        if key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return os.getenv(key, default)
```

### 2. Tratamento em páginas Streamlit
Em vez de acessar `os.getenv("XANO_SUBJECT_API_BASE")` diretamente no topo dos arquivos das páginas, utilizar `get_config("XANO_SUBJECT_API_BASE")`.

## Risks / Trade-offs

- **Execução fora do Streamlit (testes ou scripts CLI)**: A consulta a `st.secrets` pode lançar `FileNotFoundError` ou `AttributeError` se `st` não estiver rodando no contexto do servidor Streamlit. A cláusula `try/except` mitiga esse risco realizando fallback imediato para `os.getenv()`.
