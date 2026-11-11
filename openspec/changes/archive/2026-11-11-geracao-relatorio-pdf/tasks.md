# Tasks: Geração de Relatório PDF

## 1. Backend (Xano)
- [x] Criar grupo de API `report` em `api/report/report.xs`
- [x] Criar endpoint `GET /report/student-performance` em `api/report/report/student_performance_GET.xs` com autenticação `auth = "user"` filtrando `subjects` e `academic_tasks` por `$auth.id`

## 2. Script Python de Relatório PDF
- [x] Implementar script `scripts/generate_report.py` com suporte à biblioteca `reportlab` para gerar PDF de desempenho
- [x] Suportar argumentos de linha de comando (`--token`, `--api-base`, `--output`) e variáveis de ambiente (`XANO_TOKEN`, `XANO_API_BASE`)
- [x] Integrar cálculo de progresso por disciplina no script de relatório

