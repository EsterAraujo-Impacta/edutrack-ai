# Design

## Context

No ecossistema do EduTrack AI, as entidades de dados do Xano são representadas em arquivos `.xs` dentro do diretório `tables/`. O estudante precisa registrar suas obrigações acadêmicas (provas, trabalhos, lições) associadas às disciplinas (`subjects`) cadastradas. Conforme a Regra nº 1 do `@AGENTS.md`, o escopo é restrito exclusivamente ao planejamento e definição da tabela.

## Goals / Non-Goals

**Goals:**
- Projetar o arquivo de esquema XanoScript `tables/academic_tasks.xs`.
- Configurar os campos requeridos:
  - `id`: identificador primário auto-incrementado (int)
  - `user_id`: chave estrangeira para o aluno na tabela `user` (int)
  - `subject_id`: chave estrangeira para a disciplina na tabela `subjects` (int)
  - `title`: título da tarefa/obrigação acadêmica (text)
  - `description`: descrição ou orientações da atividade (text, opcional)
  - `due_date`: data de entrega ou realização (date)
  - `status`: estado da tarefa (text, com valor padrão "pending")
  - `created_at`: data e hora de registro (timestamp com default `now`)
- Configurar índices:
  - `primary` em `id`
  - `btree` em `user_id` e `subject_id` para otimização de consultas

**Non-Goals:**
- Criação de endpoints de API REST (CRUD) para tarefas acadêmicas (não solicitado pelo usuário, obedecendo à Regra nº 1 do AGENTS.md).
- Alterações em frontend (Streamlit) ou testes adicionais.
- Deploy ou push automático para o servidor Xano (Regra nº 2 do AGENTS.md).

## Decisions

### 1. Estrutura do Arquivo XanoScript (`tables/academic_tasks.xs`)
- **Decisão**: Modelar a tabela utilizando sintaxe nativa XanoScript:
  ```xs
  table "academic_tasks" {
    auth = false

    schema {
      int id {
        description = "Identificador único da tarefa acadêmica"
      }

      int user_id {
        table = "user"
        description = "FK para o estudante dono da tarefa"
      }

      int subject_id {
        table = "subjects"
        description = "FK para a disciplina correspondente"
      }

      text title {
        description = "Título da tarefa ou obrigação acadêmica"
      }

      text description? {
        description = "Descrição detalhada ou instruções da tarefa"
      }

      date due_date {
        description = "Data limite de entrega ou realização"
      }

      text status?="pending" {
        description = "Status da tarefa (ex: pending, completed, overdue)"
      }

      timestamp created_at?=now {
        description = "Data de registro da tarefa no sistema"
      }
    }

    index = [
      {type: "primary", field: [{name: "id"}]}
      {
        type : "btree"
        field: [{name: "user_id"}, {name: "subject_id"}]
      }
    ]
  }
  ```

## Risks / Trade-offs

- **[Dependência Relacional]**: A tabela `academic_tasks` depende da existência prévia da tabela `subjects` e da tabela `user`. A tabela `subjects` já teve seu esquema definido e aprovado nas especificações do projeto.
