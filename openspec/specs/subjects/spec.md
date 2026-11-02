# subjects Specification

## Purpose
Gerencia o ciclo de vida completo de disciplinas acadêmicas (subjects) para os estudantes no EduTrack AI, permitindo organização curricular e acompanhamento letivo.

## Requirements

### Requirement: Subject Creation
The system SHALL provide a POST /subjects endpoint that allows authenticated students to register a new academic subject. The system MUST associate the created subject with the authenticated student's user_id from the auth context and persist fields including name, optional teacher, and optional hours.

#### Scenario: Successful subject creation
- **WHEN** authenticated user submits valid subject data with name "Innovation Lab"
- **THEN** system persists the subject record with user_id matching auth context and returns the created subject.

#### Scenario: Validation failure on missing name
- **WHEN** authenticated user attempts to create a subject without providing a subject name
- **THEN** system rejects the creation with a descriptive validation error.

### Requirement: Subject Listing and Filtering
The system SHALL provide a GET /subjects endpoint that returns all subjects belonging exclusively to the authenticated student, filtering by user_id from auth context.

#### Scenario: Listing subjects for current user
- **WHEN** authenticated student requests the list of subjects via GET /subjects
- **THEN** system returns an array of subjects where user_id matches the authenticated user.

### Requirement: Subject Modification
The system SHALL provide a PATCH /subjects/{id} endpoint that allows authenticated students to update details of an existing subject, strictly enforcing that the target subject belongs to the authenticated user.

#### Scenario: Updating subject details
- **WHEN** authenticated student submits updated fields for an existing subject ID owned by them
- **THEN** system updates the database record and returns the updated subject entity.

#### Scenario: Rejecting modification of subject belonging to another user
- **WHEN** authenticated student attempts to update a subject ID belonging to a different user
- **THEN** system rejects the operation or returns a not found response.

### Requirement: Subject Deletion
The system SHALL provide a DELETE /subjects/{id} endpoint that allows authenticated students to remove an existing subject, strictly enforcing that the subject belongs to the authenticated user.

#### Scenario: Deleting a subject
- **WHEN** authenticated student requests deletion of an existing subject owned by them
- **THEN** system removes the subject record and confirms deletion.

#### Scenario: Rejecting deletion of subject belonging to another user
- **WHEN** authenticated student attempts to delete a subject ID belonging to a different user
- **THEN** system rejects the deletion or returns a not found response.
