# Design

## Context

O backend do EduTrack AI é modelado em XanoScript (.xs). As tabelas `subjects` (`table/subjects.xs`) e `academic_tasks` (`table/academic_tasks.xs`) já estão estruturadas no repositório, com chave estrangeira `user_id` referenciando a tabela `user`. A autenticação do sistema disponibiliza a identidade do estudante logado no contexto de requisição através de `$auth.id`.

Para a motivação detalhada, consulte `proposal.md`. Para os requisitos de comportamento e cenários, consulte os arquivos sob `specs/`.

## Goals / Non-Goals

**Goals:**
- Projetar a estrutura de diretórios e arquivos XanoScript para os grupos de API `subjects` e `academic_tasks`.
- Implementar 4 endpoints REST para `subjects`: `POST /subjects`, `GET /subjects`, `PATCH /subjects/{subjects_id}`, `DELETE /subjects/{subjects_id}`.
- Implementar 4 endpoints REST para `academic_tasks`: `POST /academic_tasks`, `GET /academic_tasks`, `PATCH /academic_tasks/{academic_tasks_id}`, `DELETE /academic_tasks/{academic_tasks_id}`.
- Garantir isolamento estrito de dados por estudante logado em todas as operações:
  - Injeção forçada de `user_id = $auth.id` na criação (POST).
  - Filtragem estrita por `user_id == $auth.id` na consulta de listas (GET).
  - Validação de propriedade (`id` e `user_id == $auth.id`) antes de mutações ou exclusões (PATCH e DELETE).
- Configurar autenticação obrigatória (`auth = ""`) em todos os endpoints.

**Non-Goals:**
- Alterações em esquemas de tabelas existentes (tabelas já definidas e estáveis).
- Implementação ou modificação de páginas Streamlit nesta fase (obedecendo à Regra nº 1 do AGENTS.md).
- Push, deploy ou sincronização remota automatizada com o Xano (vedado pela Regra nº 2 do AGENTS.md).

## Decisions

### 1. Estrutura de Diretórios e Grupos de API XanoScript
- **Decisão**: Criar dois grupos dedicados no diretório `api/`:
  - `api/subjects/`:
    - `subjects.xs`: Definição do `api_group "subjects"`
    - `subjects_POST.xs`: Adicionar disciplina
    - `subjects_GET.xs`: Listar disciplinas do usuário
    - `subjects/subjects_id_PATCH.xs`: Atualizar disciplina do usuário
    - `subjects/subjects_id_DELETE.xs`: Excluir disciplina do usuário
  - `api/academic_tasks/`:
    - `academic_tasks.xs`: Definição do `api_group "academic_tasks"`
    - `academic_tasks_POST.xs`: Adicionar tarefa
    - `academic_tasks_GET.xs`: Listar tarefas do usuário
    - `academic_tasks/academic_tasks_id_PATCH.xs`: Atualizar tarefa do usuário
    - `academic_tasks/academic_tasks_id_DELETE.xs`: Excluir tarefa do usuário
- **Alternativa descartada**: Mesclar todos os endpoints sob um grupo genérico existente (`event_logs`). Foi descartada por violar a coesão de domínio do projeto.

### 2. Segurança e Isolamento Multi-Tenant ($auth.id)
- **Decisão**: 
  - Todo endpoint declarará `auth = ""` para exigir token JWT de autenticação válido.
  - No `POST`, o `user_id` não será recebido como input modificável do usuário; será atribuído diretamente a partir de `$auth.id`.
  - No `GET`, a cláusula de busca aplicará filtro direto:
    ```xs
    where = ($db.subjects.user_id == $auth.id)
    ```
  - No `PATCH` e `DELETE`, a busca e a alteração/remoção só afetarão registros onde `id == $input.id` e `user_id == $auth.id`. Caso o registro não exista ou pertença a outro usuário, a API lançará erro (ex: `precondition` ou 404), mitigando vulnerabilidades IDOR (Insecure Direct Object References).

### 3. Validação Cruzada de Chaves Estrangeiras em academic_tasks
- **Decisão**: Ao criar ou atualizar uma tarefa acadêmica com `subject_id`, a API verificará se a disciplina informada pertence ao mesmo `$auth.id`, evitando vincular tarefas a matérias de outros estudantes.

## Risks / Trade-offs

- **[Vulnerabilidade IDOR em PATCH/DELETE]** → Mitigação: Em operações por ID, validar sempre se `user_id` do registro coincide com `$auth.id` antes de persistir mutações ou exclusões.
- **[Tentativa de sobrescrita de user_id via payload]** → Mitigação: Desconsiderar qualquer parâmetro `user_id` vindo do corpo da requisição e atribuir explicitamente `$auth.id` nas operações de escrita.

