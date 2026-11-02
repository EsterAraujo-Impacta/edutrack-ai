# academic-tasks Specification

## Purpose

Gerencia as operações de ciclo de vida e endpoints REST de tarefas e obrigações acadêmicas no EduTrack AI, garantindo integridade relacional e isolamento estrito por usuário autenticado.

## ADDED Requirements

### Requirement: Academic Task Creation
The system SHALL provide a POST /academic_tasks endpoint that allows authenticated students to register a new academic task. The system MUST associate the task with the authenticated user's user_id from the auth context and persist fields including title, optional description, due_date, status defaulting to pending, and subject_id.

#### Scenario: Successful academic task creation
- **WHEN** authenticated user submits valid task data with title "Laboratório 1" and subject_id
- **THEN** system persists the task record with user_id matching auth context and returns the created task.

#### Scenario: Validation failure on missing required fields
- **WHEN** authenticated user attempts to create a task without providing required fields such as title or subject_id
- **THEN** system rejects the creation with a descriptive validation error.

### Requirement: Academic Task Listing
The system SHALL provide a GET /academic_tasks endpoint that returns all academic tasks belonging exclusively to the authenticated student, filtering by user_id from auth context.

#### Scenario: Listing academic tasks for current user
- **WHEN** authenticated student requests the list of tasks via GET /academic_tasks
- **THEN** system returns an array of academic tasks where user_id matches the authenticated user.

### Requirement: Academic Task Modification
The system SHALL provide a PATCH /academic_tasks/{id} endpoint that allows authenticated students to update fields of an existing task, strictly enforcing that the target task belongs to the authenticated user.

#### Scenario: Updating academic task details
- **WHEN** authenticated student submits updated fields for an existing task ID owned by them
- **THEN** system updates the database record and returns the updated task entity.

#### Scenario: Rejecting modification of task belonging to another user
- **WHEN** authenticated student attempts to update a task ID belonging to a different user
- **THEN** system rejects the operation or returns a not found response.

### Requirement: Academic Task Deletion
The system SHALL provide a DELETE /academic_tasks/{id} endpoint that allows authenticated students to remove an existing academic task, strictly enforcing that the task belongs to the authenticated user.

#### Scenario: Deleting an academic task
- **WHEN** authenticated student requests deletion of an existing task owned by them
- **THEN** system removes the task record and confirms deletion.

#### Scenario: Rejecting deletion of task belonging to another user
- **WHEN** authenticated student attempts to delete a task ID belonging to a different user
- **THEN** system rejects the deletion or returns a not found response.

