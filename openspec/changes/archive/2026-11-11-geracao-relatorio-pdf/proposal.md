# Proposal: Geração de Relatório PDF

## Why

Atualmente, o EduTrack AI permite acompanhar tarefas e calcular o progresso acadêmico por disciplina via script/API, mas não oferece um recurso consolidado para exportação formal em documento portátil (PDF). O aluno ou professor precisa de um relatório em PDF estruturado com o desempenho escolar (disciplinas, status das tarefas, percentual de conclusão) e de um endpoint no Xano para viabilizar o download ou obtenção desses dados.

## What Changes

- Criação de um script Python em `scripts/generate_report.py` utilizando a biblioteca `reportlab` para gerar o arquivo PDF com o desempenho acadêmico do aluno.
- Criação de endpoint no Xano (`GET /report/student-performance`) no grupo de API `report` para viabilizar a recuperação/download do relatório consolidado do estudante autenticado.

## Capabilities

### New Capabilities
- `geracao-relatorio-pdf`: Geração de relatório PDF de desempenho do aluno (disciplinas e progresso de tarefas) e disponibilização via endpoint no Xano.

### Modified Capabilities
- Nenhuma.

## Impact

- **Scripts Python**: Adição de `scripts/generate_report.py`.
- **Backend (Xano)**: Criação do grupo de API `api/report/report.xs` e endpoint `api/report/report/student_performance_GET.xs`.
- **Dependências**: Requer `reportlab` no ambiente Python.

