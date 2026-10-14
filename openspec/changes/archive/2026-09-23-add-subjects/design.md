# Design

## Context

O EduTrack AI é composto por um frontend em Streamlit (`app.py`) e um backend em Xano (tabelas, funções e endpoints de API). Veja `proposal.md` para a motivação e escopo geral. Atualmente a interface do Streamlit possui apenas placeholders nas seções "Disciplinas" e "Dashboard", sem camada de dados persistente para matérias.

## Goals / Non-Goals

**Goals:**
- Projetar o schema da tabela `subjects` no Xano com campos essenciais e tipagem adequada.
- Definir os contratos REST para o grupo de API `/subjects` (GET, POST, PUT, DELETE).
- Projetar a interface de usuário no Streamlit para listar disciplinas em formato de cards, permitir cadastro via formulário e atualizar o contador de disciplinas ativas no Dashboard.
- Disponibilizar uma camada de serviço com fallback/mock para testes locais no Streamlit enquanto os endpoints do Xano estiverem sendo sincronizados.

**Non-Goals:**
- Gestão de tarefas e prazos atrelados às disciplinas (será abordado em `add-tasks`).
- Cálculo e simulação de média/ponderação de notas por disciplina (funcionalidade futura).
- Importação automática de grades horárias a partir de sistemas universitários externos.

## Decisions

### 1. Modelo de Dados da Tabela `subjects`
- **Decisão**: Criar uma tabela dedicada `subjects` no Xano com:
  - `id`: integer (chave primária auto-incrementada)
  - `user_id`: integer (referência ao usuário/estudante autenticado)
  - `name`: text (nome da disciplina, obrigatório)
  - `code`: text (sigla/código da matéria, ex.: "LAB01", opcional)
  - `professor`: text (nome do docente, opcional)
  - `semester`: text (período letivo, ex.: "2026.2", obrigatório)
  - `workload_hours`: integer (carga horária total em horas, opcional)
  - `status`: text (enum: `active`, `completed`, `dropped`, padrão `active`)
  - `color`: text (código hexadecimal para identificação visual no frontend, ex.: `#4A90E2`)
  - `created_at`: timestamp
- **Alternativas consideradas**: Salvar como array JSON dentro do registro de `user`. Rejeitado para permitir índices eficientes, integridade relacional e futuras relações com tarefas, faltas e avaliações.

### 2. Endpoints da API Xano
- **Decisão**: Grupo de API `/subjects`:
  - `GET /subjects`: Lista disciplinas do usuário autenticado (com filtro opcional por `status` e `semester`).
  - `POST /subjects`: Cria nova disciplina com validação dos campos obrigatórios.
  - `GET /subjects/{id}`: Retorna detalhes de uma disciplina específica.
  - `PUT /subjects/{id}`: Atualiza os dados de uma disciplina existente.
  - `DELETE /subjects/{id}`: Remove uma disciplina.
- **Alternativas consideradas**: Usar apenas GraphQL ou RPC. Rejeitado para manter o padrão REST idiomático do Xano.

### 3. Integração com o Frontend (Streamlit)
- **Decisão**: Estruturar um módulo `services/subjects_service.py` que abstrai as chamadas HTTP para o Xano. Se as credenciais do Xano não estiverem presentes no ambiente (`.env` ou `st.secrets`), o serviço opera em modo demonstrativo/local (armazenando em `st.session_state`), permitindo desenvolvimento ágil e testes imediatos.
- **Alternativas consideradas**: Chamadas `requests.get/post` diretas no corpo de `app.py`. Rejeitado para evitar acoplamento da camada visual com a infraestrutura de rede.

## Risks / Trade-offs

- **[Dependência de credenciais Xano no Streamlit]** → *Mitigação*: Implementar modo offline/mock no `subjects_service.py` com fallback automático quando variáveis de ambiente do Xano não estiverem configuradas.
- **[Orquestração com regras do AGENTS.md para XanoScript]** → *Mitigação*: Definir esquemas e endpoints para delegação aos agentes especializados (`Xano Table Designer` e `Xano API Query Writer`) conforme estipulado nas diretrizes do projeto.
