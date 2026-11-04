# Spec Delta

## Purpose

Define os requisitos de autenticação do EduTrack AI: registro de novo usuário, login e consulta de perfil do usuário autenticado, integrando o frontend Streamlit com os endpoints Xano de autenticação.

## ADDED Requirements

### Requirement: User Registration

The system SHALL allow a new user to register an account by providing email and password via the `POST /auth/signup` endpoint. The email and password MUST be mandatory fields. An optional name field MAY also be accepted.

#### Scenario: Successful registration

- **WHEN** user submits a valid email and password via the signup form
- **THEN** the system sends a POST request to `{XANO_API_BASE}/auth/signup` and shows a success message upon receiving a 200 response.

#### Scenario: Validation failure on empty fields

- **WHEN** user submits the signup form with an empty email or password
- **THEN** the system SHALL show a validation error message and SHALL NOT call the Xano API.

#### Scenario: API error on registration

- **WHEN** the Xano API returns an HTTP error (e.g., email already in use)
- **THEN** the system SHALL display the error message returned by the API to the user.

---

### Requirement: User Login

The system SHALL allow a registered user to authenticate by providing email and password via the `POST /auth/login` endpoint. Upon success, the JWT token returned MUST be stored in `st.session_state` for use in subsequent authenticated requests.

#### Scenario: Successful login

- **WHEN** user submits valid credentials via the login form
- **THEN** the system sends a POST request to `{XANO_API_BASE}/auth/login`, receives a JWT token in the response, stores it in `st.session_state["jwt_token"]`, and shows a success message.

#### Scenario: Invalid credentials

- **WHEN** user submits incorrect email or password
- **THEN** the system SHALL display the error message returned by the Xano API and SHALL NOT store any token.

---

### Requirement: Current User Profile

The system SHALL retrieve and display the authenticated user's profile data by calling `GET /auth/me` with the stored JWT token. This section SHALL only be rendered when a JWT token exists in `st.session_state`.

#### Scenario: Profile displayed after login

- **WHEN** a JWT token is present in `st.session_state`
- **THEN** the system sends a GET request to `{XANO_API_BASE}/auth/me` with the header `Authorization: Bearer <token>` and displays the returned user data.

#### Scenario: No token present

- **WHEN** no JWT token is stored in `st.session_state`
- **THEN** the profile section SHALL display an informational message prompting the user to log in, and SHALL NOT call `/auth/me`.

---

### Requirement: Base URL Configuration

The system SHALL read the Xano API base URL from an environment variable `XANO_API_BASE` defined in a `.env` file at the project root. The application MUST NOT start if `XANO_API_BASE` is not set.

#### Scenario: .env configured correctly

- **WHEN** `.env` contains a valid `XANO_API_BASE` value
- **THEN** `auth_helper.py` loads it via `python-dotenv` and uses it as the base for all API calls.

#### Scenario: Missing XANO_API_BASE

- **WHEN** `XANO_API_BASE` is not set in the environment
- **THEN** `auth_helper.py` SHALL raise a `RuntimeError` with a descriptive message.

