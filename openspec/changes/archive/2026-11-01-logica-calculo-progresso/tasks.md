# Tasks

## 1. Implementação do Script de Cálculo de Progresso (Python)

- [x] 1.1 Criar o diretório `scripts/` e o arquivo `scripts/calculate_progress.py` contendo a função de consulta às tarefas da disciplina via endpoint CRUD `GET /academic_tasks`
- [x] 1.2 Implementar a lógica de cálculo da porcentagem de progresso (`concluídas / total * 100`) com proteção contra divisão por zero quando não houver tarefas
- [x] 1.3 Implementar a formatação e estruturação da saída em JSON com `subject_id`, `total_tasks`, `completed_tasks`, `progress_percentage` e `status`
- [x] 1.4 Adicionar interface de linha de comando (`argparse`) no script e verificar a execução com teste automatizado da saída JSON
