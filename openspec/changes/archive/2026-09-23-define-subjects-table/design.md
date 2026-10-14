# Design

## Context

Conforme estabelecido no `@AGENTS.md`, o desenvolvimento no Xano é modular e focado estritamente no escopo solicitado pelo usuário. O usuário solicitou a definição do esquema da tabela `subjects`. Tabelas no XanoScript são definidas na pasta `tables/` através de arquivos `.xs`.

## Goals / Non-Goals

**Goals:**
- Criar a definição formal da tabela `subjects` em `tables/subjects.xs`.
- Configurar os campos: `id` (int, auto/PK), `name` (text), `teacher` (text), `hours` (int com filtro de mínimo 0), `user_id` (int com relacionamento para a tabela `user`).
- Configurar os índices: `primary` para `id` e `btree` para `user_id`.

**Non-Goals:**
- Criação de endpoints de API (CRUD) para subjects (proibido pela regra de escopo do `AGENTS.md` sem solicitação explícita).
- Criação de testes unitários ou alterações no frontend (Streamlit).
- Deploy ou push automático para o Xano (responsabilidade manual do desenvolvedor conforme `AGENTS.md`).

## Decisions

### 1. Definição do Arquivo XanoScript (`tables/subjects.xs`)
- **Decisão**: Utilizar a sintaxe nativa do XanoScript:
  ```xs
  table "subjects" {
    auth = false
    schema {
      int id {
        description = "Identificador único da disciplina"
      }
      text name {
        description = "Nome da disciplina"
      }
      text teacher {
        description = "Nome do professor responsável"
      }
      int hours filters=min:0 {
        description = "Carga horária da matéria em horas"
      }
      int user_id {
        table = "user"
        description = "FK para a tabela de autenticação do Xano: user"
      }
    }
    index = [
      {type: "primary", field: [{name: "id"}]}
      {
        type : "btree"
        field: [{name: "user_id"}]
      }
    ]
  }
  ```
- **Alternativas consideradas**: Criar apenas documentação em markdown. Rejeitado pois a diretriz autoriza explicitamente criar arquivos `.xs`.

## Risks / Trade-offs

- **[Dependência da tabela user existir no workspace Xano]** → *Mitigação*: A tabela `user` é a tabela padrão de autenticação do Xano quick-start já presente no projeto.
