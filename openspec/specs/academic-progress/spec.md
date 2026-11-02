# academic-progress Specification

## Purpose
Define a lógica de negócio e o formato de saída para o cálculo e monitoramento do progresso acadêmico do estudante em cada disciplina com base nas tarefas associadas no EduTrack AI.

## Requirements

### Requirement: Subject Progress Calculation
The system SHALL calculate the academic progress of a subject as the ratio of completed tasks to total tasks expressed as a percentage. When a subject has zero tasks, the system MUST return 0.0 percent without division by zero errors.

#### Scenario: Calculating progress with mixed task statuses
- **WHEN** progress is calculated for a subject with 3 completed tasks out of 4 total tasks
- **THEN** system returns 75.0 percent progress.

#### Scenario: Calculating progress for subject without tasks
- **WHEN** progress is calculated for a subject that has 0 registered tasks
- **THEN** system returns 0.0 percent progress without throwing an arithmetic error.

### Requirement: JSON Output Formatting
The system SHALL output the calculated progress in valid JSON format containing subject_id, total_tasks, completed_tasks, progress_percentage, and completion_status.

#### Scenario: Formatting successful progress result
- **WHEN** subject progress is calculated successfully
- **THEN** system generates a JSON document containing subject_id, total_tasks, completed_tasks, progress_percentage, and completion_status.

### Requirement: CRUD Endpoint Integration
The system SHALL retrieve academic tasks for the target subject by querying the academic tasks CRUD endpoint or client using the user's authentication context.

#### Scenario: Fetching tasks via CRUD endpoint
- **WHEN** progress calculation is triggered for a valid subject ID
- **THEN** system queries the academic tasks endpoint with subject_id and user authentication to fetch relevant tasks.
