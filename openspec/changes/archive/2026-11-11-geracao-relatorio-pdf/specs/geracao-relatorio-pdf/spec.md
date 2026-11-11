# geracao-relatorio-pdf Specification

## Purpose

Definir os requisitos para a geração de relatório de desempenho acadêmico do aluno em formato PDF via script Python e para o endpoint do Xano que disponibiliza os dados/download desse relatório.

## ADDED Requirements

### Requirement: Geração de Relatório PDF via Script Python

The system SHALL provide a Python script at `scripts/generate_report.py` that collects the student's academic progress data from the Xano backend and generates a formatted PDF document using the `reportlab` library.

#### Scenario: Geração bem-sucedida do PDF com disciplinas e tarefas
- **WHEN** user executes `scripts/generate_report.py` with valid credentials/token and an output path
- **THEN** system SHALL calculate progress for each subject and output a formatted PDF report containing student information, subjects, task completion stats, and progress percentages.

#### Scenario: Execução sem token ou credenciais de acesso
- **WHEN** user executes `scripts/generate_report.py` without providing an authentication token or base URL
- **THEN** system SHALL terminate execution with exit code 1 and output an error message to stderr.

### Requirement: Endpoint Xano para Baixar Relatório de Desempenho

The system SHALL expose an authenticated endpoint `GET /report/student-performance` within the `report` API group in Xano to provide the student's performance report.

#### Scenario: Requisição autenticada do relatório
- **WHEN** authenticated user calls `GET /report/student-performance` with a valid JWT
- **THEN** system SHALL query the student's user record, registered subjects, and academic tasks filtered by `user_id == $auth.id` and return the consolidated report data.

#### Scenario: Requisição não autenticada
- **WHEN** an unauthenticated request attempts to call `GET /report/student-performance`
- **THEN** system SHALL reject the request with HTTP 401 Unauthorized.

