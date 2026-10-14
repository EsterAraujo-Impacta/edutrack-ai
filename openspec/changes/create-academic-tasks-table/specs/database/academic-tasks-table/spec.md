# academic-tasks-table Specification

## Purpose

Define a estrutura e o modelo de dados da tabela academic_tasks no Xano para persistência e gestão de obrigações acadêmicas (lições, provas, trabalhos) vinculadas às disciplinas dos alunos.

## ADDED Requirements

### Requirement: Academic Tasks Table Schema Definition
The database SHALL define the `academic_tasks` table in XanoScript syntax with fields `id` (int primary key), `title` (text), `description` (text optional), `due_date` (date), `status` (text with default "pending"), `subject_id` (int foreign key to `subjects`), and `user_id` (int foreign key to `user`).

#### Scenario: Validating academic tasks table schema structure
- **WHEN** the table definition for `academic_tasks` is evaluated
- **THEN** it defines `id` as primary key, `title` as mandatory text, `description` as optional text, `due_date` as date, `status` as text defaulting to "pending", `subject_id` referencing the `subjects` table, and `user_id` referencing the `user` table.

#### Scenario: Validating academic tasks table indexes
- **WHEN** table indexes are inspected
- **THEN** there is a primary index on `id` and btree indexes on `user_id` and `subject_id`.
