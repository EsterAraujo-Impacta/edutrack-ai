# Change: cadastro-login

# Proposal

## Why

Atualmente o EduTrack AI não possui autenticação de usuários. A plataforma não tem tela de cadastro nem de login, o que impede o controle de quem acessa os dados e a associação de disciplinas, tarefas e notas a um estudante específico. Para que qualquer dado do sistema seja persistido de forma segura e vinculada ao usuário correto no Xano, é necessário implementar o fluxo de registro e autenticação.

## What Changes

- Adição da página `pages/3_👤_Perfil.py` com formulários de cadastro e login via Streamlit.
- Criação de `pages/auth_helper.py`, módulo reutilizável com helpers HTTP (`post`, `get`) que carregam a URL base do `.env` e injetam o cabeçalho `Authorization: Bearer <token>` automaticamente.
- Criação do arquivo `.env` na raiz do projeto com a variável `XANO_API_BASE`.
- Integração com os endpoints Xano `POST /auth/signup`, `POST /auth/login` e `GET /auth/me`.
- Armazenamento do JWT retornado no login no `st.session_state` do Streamlit.

## Capabilities

### New Capabilities
- `cadastro-login`: Permite ao usuário criar conta, entrar na plataforma e visualizar seu perfil via endpoints de autenticação do Xano.

### Modified Capabilities
- Nenhuma modificação em capabilities existentes.

## Impact

- **Frontend (Streamlit)**: Nova página `pages/3_👤_Perfil.py` e helper `pages/auth_helper.py`.
- **Configuração**: Novo arquivo `.env` na raiz do projeto.
- **APIs**: Consumo dos endpoints Xano `auth/signup`, `auth/login` e `auth/me`.
- **Segurança**: O token JWT ficará armazenado em `st.session_state` durante a sessão.

