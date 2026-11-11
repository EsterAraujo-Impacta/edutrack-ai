# Design: Geração de Relatório PDF e Endpoint Xano

## Context

O EduTrack AI gerencia disciplinas (`subjects`) e tarefas (`academic_tasks`), com autenticação via tabela `user` e cálculo de progresso em `scripts/calculate_progress.py`. Este design planeja o script Python com `reportlab` e o endpoint no backend Xano para consolidar e baixar/exportar os dados de desempenho acadêmico do aluno.

## Goals / Non-Goals

**Goals:**
- Script Python em `scripts/generate_report.py` para gerar relatório PDF consolidando: dados do aluno, disciplinas ativas, tarefas concluídas vs. pendentes e porcentagem de progresso.
- Suporte a geração local com `reportlab` (gerando tabelas limpas e cabeçalho com dados do aluno).
- Endpoint Xano `GET /report/student-performance` que busca `user`, `subjects` e `academic_tasks` filtrando obrigatoriamente por `user_id == $auth.id`.

**Non-Goals:**
- Armazenamento de PDFs pré-gerados em bucket de armazenamento de longo prazo (geração sob demanda).
- Envio de relatório por e-mail no MVP.

## Decisions

### 1. Biblioteca para Geração de PDF
- **Decisão**: Utilizar `reportlab` no script Python `scripts/generate_report.py`.
- **Motivo**: Biblioteca padrão e amplamente utilizada para criação programática de PDFs com tabelas e estilos customizados sem requerer headless browsers.

### 2. Integração e Reaproveitamento de Regras de Progresso
- **Decisão**: O script `scripts/generate_report.py` reutilizará ou seguirá a mesma lógica de status e cálculo de `scripts/calculate_progress.py` (`completed`, `concluida`, `done`).
- **Autenticação**: Suporte a parâmetros `--token`, `--api-base`, `--output` e variáveis de ambiente `XANO_TOKEN` / `XANO_API_BASE`.

### 3. Endpoint Xano (`api/report/report/student_performance_GET.xs`)
- **Decisão**:
  - Pertencente ao grupo `report` (`api/report/report.xs`).
  - Autenticado com `auth = "user"`.
  - Filtro rígido por `$auth.id` em `subjects` e `academic_tasks`.
  - Retorna o payload consolidado (`user`, `subjects`, `tasks`) para possibilitar tanto o download direto dos dados quanto o consumo por clientes/scripts geradores de PDF.

## Risks / Trade-offs

- **Dependência do reportlab**: Caso `reportlab` não esteja instalado no ambiente Python, o script deve emitir mensagem descritiva de erro e orientar a instalação via `pip install reportlab`.
- **Segurança de Dados**: O endpoint no Xano deve sempre validar `auth = "user"` e filtrar todas as consultas por `$auth.id` para garantir isolamento multitenant entre estudantes.

