# Change: feature-notas-atividades

## Why

Atualmente no EduTrack AI, não há funcionalidade para que professores possam registrar e lançar notas obtidas pelos alunos em atividades acadêmicas específicas. A introdução desta funcionalidade permite o registro formal de notas atreladas aos estudantes e às atividades avaliativas.

## What Changes

- Criação da tabela de banco de dados `activity_grades` no backend Xano.
- Criação do endpoint da API `POST /activity_grades` para permitir o lançamento e registro de notas de atividades por professores.
- Definição dos campos essenciais para registro de notas: `id`, `user_id` (aluno), `activity_id` (ou `academic_task_id`), `grade` (nota atribuída), `feedback` (comentários opcionais) e `graded_by` (professor que lançou a nota).

## Capabilities

### New Capabilities
- `activity-grades`: Capacidade que permite ao professor lançar notas para os alunos em atividades acadêmicas específicas.

### Modified Capabilities

## Impact

- **Backend (Xano)**: Criação da tabela `activity_grades` e criação do endpoint REST `POST /activity_grades`.
- **Banco de Dados**: Nova entidade relacional vinculando alunos, atividades e notas.
