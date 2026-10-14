# Spec Delta

## Purpose

Define a estrutura e integridade de dados da tabela subjects no Xano, estabelecendo o modelo relacional vinculado à tabela de usuários.

## ADDED Requirements

### Requirement: Subjects Table Schema Definition
The database SHALL define the `subjects` table in XanoScript syntax with fields `id` (int primary key), `name` (text), `teacher` (text), `hours` (int), and `user_id` (int foreign key to Xano `user` table).

#### Scenario: Validating table schema structure
- **WHEN** the table definition for `subjects` is evaluated
- **THEN** it defines `id` as primary key, `name` as text, `teacher` as text, `hours` as non-negative integer, and `user_id` referencing the `user` table.

#### Scenario: Index configuration
- **WHEN** table indexes are checked
- **THEN** there is a primary index on `id` and a btree index on `user_id`.
