# Design

## Context

Conforme as regras do `@AGENTS.md`, o escopo desta funcionalidade é focado estritamente no que foi solicitado: permitir que o professor lance notas para alunos em atividades específicas. Veja `proposal.md` para contexto e escopo.

## Goals / Non-Goals

**Goals:**
- Projetar o schema da tabela `activity_grades` no Xano:
  - `id`: integer (PK auto)
  - `user_id`: integer (FK para `user` - aluno avaliado)
  - `activity_id`: integer (identificador da atividade avaliada)
  - `grade`: decimal (nota atribuída)
  - `feedback`: text (comentários ou observações do professor, opcional)
  - `graded_by`: integer (FK para `user` - professor autenticado)
  - `created_at`: timestamp
- Projetar a API `POST /activity_grades` para que o professor lance a nota.

**Non-Goals:**
- Não criar endpoints de consulta (GET /academic_tasks/{id}/grades ou GET /users/{id}/grades) pois não foram solicitados pelo usuário (Regra nº 1 do AGENTS.md).
- Não criar interface frontend nem testes adicionais não solicitados.
- Não executar push ou deploy para o Xano (Regra nº 2 do AGENTS.md).

## Decisions

### 1. Tabela `activity_grades`
- Criada no Xano com chave primária `id` e chaves estrangeiras `user_id` e `graded_by` apontando para a tabela `user`.

### 2. Endpoint `POST /activity_grades`
- Recebe payload JSON:
  - `user_id` (obrigatório, aluno)
  - `activity_id` (obrigatório, atividade)
  - `grade` (obrigatório, valor numérico)
  - `feedback` (opcional, texto)
- Atribui `graded_by` com base no usuário autenticado no token de autenticação.

## Risks / Trade-offs

- **[Controle de Permissão]**: Garantir que apenas usuários com papel de professor possam submeter notas através da validação de autenticação e papel (role) no Xano.
