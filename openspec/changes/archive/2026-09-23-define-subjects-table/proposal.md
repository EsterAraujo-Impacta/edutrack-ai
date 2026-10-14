# Change: feature-notas-atividades

# Proposal

## Why

Seguindo as diretrizes de desenvolvimento do `@AGENTS.md`, é necessário definir formalmente o esquema da tabela `subjects` no backend Xano para suportar o cadastro de disciplinas pelos estudantes no EduTrack AI.

## What Changes

- Criação da definição de esquema da tabela `subjects` em formato XanoScript (`tables/subjects.xs`).
- Definição dos campos especificados pelo usuário:
  - `id`: identificador único com auto-incremento (PK)
  - `name`: nome da disciplina (text)
  - `teacher`: nome do professor responsável (text)
  - `hours`: carga horária da disciplina em horas (int)
  - `user_id`: chave estrangeira referenciando a tabela de autenticação de usuários do Xano (`user`)
- Criação dos índices da tabela (`primary` em `id` e `btree` em `user_id`).
- Em conformidade estrita com o `@AGENTS.md`, o escopo é restrito exclusivamente à definição da tabela de dados solicitada, sem criação automática de API CRUD, testes ou frontend.

## Capabilities

### New Capabilities
- `database/subjects-table`: Esquema estruturado e integridade referencial da tabela `subjects` no Xano.

### Modified Capabilities

## Impact

- **Backend / Banco de Dados**: Adição do arquivo de definição de tabela `tables/subjects.xs` no projeto Xano.
