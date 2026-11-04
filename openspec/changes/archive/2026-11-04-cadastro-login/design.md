# Design

## Context

O EduTrack AI utiliza Streamlit no frontend e Xano no backend. O Xano fornece endpoints de autenticação padrão (`auth/signup`, `auth/login`, `auth/me`) que retornam JWT. O frontend precisa de uma página dedicada de perfil/autenticação e de um módulo helper reutilizável para chamadas HTTP autenticadas.

## Goals / Non-Goals

**Goals:**
- Criar a página Streamlit `pages/3_👤_Perfil.py` com formulários de cadastro e login.
- Criar `pages/auth_helper.py` com funções genéricas `post` e `get` que injetam o cabeçalho de autenticação quando um token for fornecido.
- Carregar a URL base do Xano a partir de `.env` usando `python-dotenv`.
- Armazenar o JWT no `st.session_state` para persistência durante a sessão Streamlit.

**Non-Goals:**
- Logout (invalidação de sessão no servidor Xano).
- Refresh automático de token expirado.
- Gestão de papéis/permissões (admin, professor, aluno).

## Decisions

### 1. Módulo `pages/auth_helper.py`

- **Decisão**: Criar um módulo separado (não embutido na página) para permitir reuso em outras páginas futuras que precisem de chamadas autenticadas.
- **Implementação**:
  - Usa `urllib.request` (stdlib) — sem dependências externas além de `python-dotenv`.
  - `post(endpoint, payload, token=None)` → faz POST com JSON e injeta `Authorization` se token presente.
  - `get(endpoint, token)` → faz GET com `Authorization`.
  - Erros HTTP e de rede são capturados e relançados como `RuntimeError` com mensagem legível.
- **Alternativas consideradas**: Usar a biblioteca `requests`. Rejeitado para manter zero dependências extras além das já existentes no projeto.

### 2. Persistência do JWT

- **Decisão**: Armazenar o token em `st.session_state["jwt_token"]`.
- **Motivo**: O Streamlit re-executa o script a cada interação; o `session_state` é o mecanismo nativo para estado entre interações dentro de uma mesma sessão.
- **Escrita opcional em `.auth_token`**: Para facilitar depuração e uso em scripts externos (ex.: `calculate_progress.py --token`), o token também é escrito no arquivo `.auth_token` na raiz do projeto (falha silenciosamente se não for possível).

### 3. Arquivo `.env`

- **Decisão**: Criar `.env` na raiz do projeto com `XANO_API_BASE=https://<instancia>.xano.io/api`.
- **`auth_helper.py`** resolve o caminho do `.env` relativamente a sua própria localização (`../` em relação a `pages/`).
- **`.gitignore`**: O `.env` DEVE ser listado no `.gitignore` para não expor credenciais.

### 4. Estrutura da Página `pages/3_👤_Perfil.py`

```
st.title("👤 Perfil do Usuário")
├── st.header("Cadastrar nova conta")   → form: email, senha, nome (opcional)
├── st.header("Login")                 → form: email, senha
└── [se token presente]
    └── st.header("Dados do usuário atual") → st.json(resultado de /auth/me)
```

## Risks / Trade-offs

- **[Token expira durante a sessão]** → *Mitigação*: Exibir mensagem de erro amigável quando `/auth/me` retornar 401 e sugerir novo login.
- **[`.env` não configurado]** → *Mitigação*: `auth_helper.py` lança `RuntimeError` descritivo na importação.
- **[Senha em texto plano no Streamlit]** → *Mitigação*: Usar `st.text_input(..., type="password")` para mascarar a senha na UI.

