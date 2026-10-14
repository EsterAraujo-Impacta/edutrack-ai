# activity-grades Specification

## Purpose

Define as estruturas e regras de negócio para que professores possam registrar e lançar notas de alunos em atividades específicas no EduTrack AI.

## ADDED Requirements

### Requirement: Record Activity Grade
The system SHALL allow authenticated instructors to submit and record a grade and optional feedback for a student on a specific academic activity via POST /activity_grades.

#### Scenario: Successful grade submission
- **WHEN** instructor submits valid grade payload containing student user_id, activity_id, and numeric grade
- **THEN** system creates the grade record in activity_grades table and returns the created record.

#### Scenario: Validation failure on missing fields
- **WHEN** instructor submits a grade payload without required fields such as student user_id or activity_id
- **THEN** system rejects the submission with a validation error.
