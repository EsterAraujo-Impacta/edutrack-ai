# subjects Specification

## Purpose
Gerencia o ciclo de vida completo de disciplinas acadêmicas (subjects) para os estudantes no EduTrack AI, permitindo organização curricular e acompanhamento letivo.

## Requirements

### Requirement: Subject Creation
The system SHALL allow students to register a new academic subject with name, optional code, professor name, semester/period, workload hours, status (active, completed, dropped), and display color. The subject name and semester MUST be mandatory fields.

#### Scenario: Successful subject creation
- **WHEN** user submits valid subject data with name "Innovation Lab" and semester "2026.2"
- **THEN** system persists the subject and returns the created subject record with an assigned ID and active status.

#### Scenario: Validation failure on missing name
- **WHEN** user attempts to create a subject without providing a subject name
- **THEN** system rejects the creation with a descriptive validation error.

### Requirement: Subject Listing and Filtering
The system SHALL provide a list of all subjects associated with the authenticated student, supporting retrieval of active, completed, or all registered subjects.

#### Scenario: Listing subjects for current user
- **WHEN** student requests the list of subjects
- **THEN** system returns an array of subjects belonging to that student, ordered by academic period and name.

### Requirement: Subject Modification
The system SHALL allow students to update details of an existing subject, including changing status, professor, or workload.

#### Scenario: Updating subject details
- **WHEN** student submits updated fields for an existing subject ID
- **THEN** system updates the database record and returns the updated subject entity.

### Requirement: Subject Deletion
The system SHALL allow students to remove a subject from their course tracking.

#### Scenario: Deleting a subject
- **WHEN** student requests deletion of an existing subject
- **THEN** system removes the subject record and confirms deletion.
