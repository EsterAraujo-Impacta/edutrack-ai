# Proposal

## Why

No EduTrack AI, os estudantes precisam acompanhar o andamento e a evolução de seus estudos em cada disciplina matriculada. Com os endpoints CRUD de disciplinas (`subjects`) e tarefas acadêmicas (`academic_tasks`) disponíveis no backend, é necessário implementar a lógica de cálculo de progresso em um script Python utilitário (`scripts/calculate_progress.py`), permitindo quantificar objetivamente o percentual de tarefas concluídas em relação ao total de tarefas de uma disciplina e retornando o resultado estruturado em formato JSON.

## What Changes

- Implementação do script Python `scripts/calculate_progress.py`.
- Criação de função para cálculo de progresso de uma disciplina específica com base em suas tarefas (`completed_tasks / total_tasks * 100`):
  - Consulta das tarefas da disciplina utilizando o endpoint CRUD de leitura (`GET /academic_tasks` filtrado por disciplina e usuário autenticado).
  - Tratamento de cenários com zero tarefas cadastradas (evitando divisão por zero e retornando 0.0%).
  - Identificação de tarefas concluídas (status `"completed"`).
  - Formatação e retorno dos resultados em formato JSON (contendo `subject_id`, `total_tasks`, `completed_tasks`, `progress_percentage` e metadados de status).
- Interface de execução direta via linha de comando (CLI) ou importação como módulo utilitário.

## Capabilities

### New Capabilities
- `academic-progress`: Cálculo e monitoramento do progresso acadêmico do estudante baseado no percentual de conclusão de tarefas vinculadas a cada disciplina.

### Modified Capabilities

## Impact

- **Scripts Utilitários**: Criação do diretório `scripts/` e do arquivo `scripts/calculate_progress.py`.
- **APIs Consumidas**: Utilização dos endpoints autenticados de `academic_tasks` e `subjects` para obter os dados em tempo de execução.
- **Formato de Saída**: Geração de respostas padronizadas em JSON para consumo por serviços e interfaces.

