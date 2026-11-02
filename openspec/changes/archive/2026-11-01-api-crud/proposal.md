# Proposal

## Why

No EduTrack AI, as entidades de disciplinas (`subjects`) e tarefas acadêmicas (`academic_tasks`) possuem suas estruturas relacionais modeladas no banco de dados Xano, porém ainda não possuem os endpoints de API REST no backend para operações cotidianas do aplicativo. A criação dos endpoints CRUD (POST, GET, PATCH, DELETE) para ambas as tabelas viabiliza a persistência e consumo dinâmico dos dados, garantindo isolamento estrito para que cada estudante visualize, edite e gerencie exclusivamente seus próprios registros acadêmicos.

## What Changes

- Implementação de endpoints REST protegidos por autenticação para a tabela `subjects`:
  - `POST /subjects`: Criação de disciplina associando automaticamente o `user_id` do usuário logado.
  - `GET /subjects`: Listagem de disciplinas pertencentes exclusivamente ao usuário autenticado.
  - `PATCH /subjects/{id}`: Atualização de dados de uma disciplina existente, validando que o registro pertence ao usuário autenticado.
  - `DELETE /subjects/{id}`: Exclusão de disciplina, validando a posse pelo usuário autenticado antes da remoção.
- Implementação de endpoints REST protegidos por autenticação para a tabela `academic_tasks`:
  - `POST /academic_tasks`: Criação de obrigação acadêmica associando automaticamente o `user_id` do usuário logado.
  - `GET /academic_tasks`: Listagem de tarefas acadêmicas pertencentes exclusivamente ao usuário autenticado.
  - `PATCH /academic_tasks/{id}`: Atualização de tarefa acadêmica, validando que pertence ao usuário autenticado.
  - `DELETE /academic_tasks/{id}`: Exclusão de tarefa acadêmica, validando a posse pelo usuário autenticado antes da remoção.
- Imposição de autenticação de usuário em todos os endpoints, extraindo `$auth.id` e impedindo qualquer vazamento ou modificação de dados entre estudantes distintos.

## Capabilities

### New Capabilities
- `academic-tasks`: Gerenciamento e operações CRUD para tarefas e obrigações acadêmicas do estudante, com garantia de isolamento por usuário autenticado.

### Modified Capabilities
- `subjects`: Atualização dos requisitos de CRUD para especificar os endpoints REST e reforçar o isolamento estrito por usuário autenticado em todas as operações.

## Impact

- **Backend (Xano / XanoScript)**:
  - Criação dos grupos de API e endpoints correspondentes sob o diretório `api/`.
  - Validação de autorização em todas as operações via `$auth.id`.
- **APIs e Segurança**: Garantia de não-acesso a recursos de terceiros por meio de verificação direta de `user_id`.

