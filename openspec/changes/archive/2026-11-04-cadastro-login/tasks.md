# Tasks

## 1. Configuração do Ambiente

- [x] 1.1 Criar o arquivo `.env` na raiz do projeto com `XANO_API_BASE=https://<instancia>.xano.io/api` e garantir que `.env` está listado no `.gitignore`

## 2. Módulo Helper de Autenticação

- [x] 2.1 Criar `pages/auth_helper.py` com as funções `post(endpoint, payload, token=None)` e `get(endpoint, token)` usando `urllib.request`, carregando `XANO_API_BASE` do `.env` via `python-dotenv`

## 3. Página de Perfil (Streamlit)

- [x] 3.1 Implementar formulário de cadastro em `pages/3_👤_Perfil.py` que chama `POST /auth/signup` com email, senha e nome (opcional) e exibe sucesso ou erro
- [x] 3.2 Implementar formulário de login em `pages/3_👤_Perfil.py` que chama `POST /auth/login`, armazena o JWT em `st.session_state["jwt_token"]` e exibe sucesso ou erro
- [x] 3.3 Implementar seção de perfil do usuário autenticado que chama `GET /auth/me` com o token armazenado e exibe os dados retornados (visível somente quando token presente)

