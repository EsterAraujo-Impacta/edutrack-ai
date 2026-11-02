# Design

## Context

No EduTrack AI, as tarefas acadêmicas (`academic_tasks`) possuem o atributo `status` (ex: "pending", "completed") e vinculação com a disciplina correspondente via `subject_id`. Os endpoints CRUD já fornecem acesso autenticado a esses registros. O usuário solicitou um script utilitário Python em `scripts/calculate_progress.py` que consuma esses dados e calcule o percentual de conclusão por disciplina, retornando o resultado em formato JSON.

Para a motivação, consulte `proposal.md`. Para os requisitos e cenários, consulte `specs/academic-progress/spec.md`.

## Goals / Non-Goals

**Goals:**
- Projetar e estruturar o script `scripts/calculate_progress.py`.
- Implementar a função `calculate_subject_progress` que aceita `subject_id` e calcula `(completed / total) * 100`.
- Retornar payload estruturado em JSON com `subject_id`, `total_tasks`, `completed_tasks`, `progress_percentage` e `status`.
- Tratar cenários de borda: disciplinas com 0 tarefas devem retornar 0.0% sem divisão por zero.
- Permitir consumo do endpoint CRUD `GET /academic_tasks` com token de autenticação e fallback/injeção direta de dados para testes.
- Fornecer interface CLI amigável via argumentos (`--subject-id`, `--api-base`, `--token`).

**Non-Goals:**
- Alterações nos endpoints do Xano ou no banco de dados.
- Modificações em páginas Streamlit existentes (obedecendo à Regra nº 1 do AGENTS.md).
- Push ou deploy remoto (Regra nº 2 do AGENTS.md).

## Decisions

### 1. Estrutura do Módulo Python (`scripts/calculate_progress.py`)
- **Decisão**: Desenvolver o script de forma modular e autônoma:
  - `fetch_tasks_for_subject(subject_id, api_base, auth_token)`: Realiza a chamada HTTP GET ao endpoint CRUD de tarefas acadêmicas.
  - `calculate_subject_progress(subject_id, tasks)`: Função pura de cálculo aritmético sobre a lista de tarefas.
  - `format_progress_json(...)`: Serialização em JSON com indentação legível.
  - `main()`: Interface CLI utilizando `argparse`.
- **Alternativa descartada**: Implementar apenas como script procedural descartável. Foi descartada para permitir que o serviço Streamlit ou testes possam importar as funções no futuro.

### 2. Tratamento de Requisições HTTP
- **Decisão**: Utilizar a biblioteca padrão `urllib.request` (ou `requests` se disponível) com header `Authorization: Bearer <token>`, permitindo funcionamento sem obrigar instalação de pacotes externos no ambiente CLI, e aceitar parâmetro opcional de lista de tarefas pré-carregadas para execução offline.

### 3. Modelo de Dados JSON de Saída
- **Decisão**: O JSON retornado terá a seguinte estrutura:
  ```json
  {
    "subject_id": 1,
    "total_tasks": 4,
    "completed_tasks": 3,
    "progress_percentage": 75.0,
    "status": "in_progress"
  }
  ```
  Onde `status` será:
  - `"no_tasks"` se `total_tasks == 0`
  - `"not_started"` se `progress_percentage == 0.0` e `total_tasks > 0`
  - `"in_progress"` se `0.0 < progress_percentage < 100.0`
  - `"completed"` se `progress_percentage == 100.0`

## Risks / Trade-offs

- **[Divisão por zero]** → Mitigação: Verificação explícita `if total_tasks == 0: return 0.0`.
- **[Conectividade com API no ambiente de desenvolvimento]** → Mitigação: Suporte a passagem de dados mockados via argumentos ou fallback em memória para execução de testes locais.

