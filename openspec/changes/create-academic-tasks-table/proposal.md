# Change: create-academic-tasks-table

## Why

No EduTrack AI, os estudantes precisam organizar suas obrigações acadêmicas cotidianas (como lições, provas, seminários e trabalhos) de forma vinculada a cada disciplina matriculada. A criação da tabela `academic_tasks` no backend Xano fornece a base relacional necessária para persistir e gerenciar essas tarefas.

## What Changes

- Criação da definição de esquema da tabela `academic_tasks` em XanoScript (`tables/academic_tasks.xs`).
- Configuração dos campos especificados:
  - `id`: identificador único com auto-incremento (chave primária)
  - `title`: título da obrigação acadêmica (text)
  - `description`: descrição detalhada da tarefa (text, opcional)
  - `due_date`: data limite de entrega ou realização (date)
  - `status`: status de execução da tarefa (text, ex: "pending", "completed")
  - `subject_id`: chave estrangeira referenciando a tabela `subjects` (int)
  - `user_id`: chave estrangeira referenciando o estudante autenticado na tabela `user` (int)
- Configuração de índices (`primary` em `id` e `btree` em `user_id`, `subject_id`).
- Em conformidade estrita com a Regra nº 1 do `@AGENTS.md`, o escopo deste planejamento contempla exclusivamente a definição da tabela de dados solicitada, sem inclusão automática de APIs CRUD, frontend ou testes.

## Capabilities

### New Capabilities
- `database/academic-tasks-table`: Definição do esquema e integridade relacional da tabela `academic_tasks` no Xano.

### Modified Capabilities

## Impact

- **Backend / Banco de Dados**: Criação do arquivo de definição de tabela `tables/academic_tasks.xs` no repositório.
