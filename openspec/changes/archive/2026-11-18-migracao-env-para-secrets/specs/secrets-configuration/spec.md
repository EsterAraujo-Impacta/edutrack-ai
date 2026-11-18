# secrets-configuration Specification

## Purpose

Define the configuration retrieval behavior for the EduTrack AI Streamlit application, prioritizing Streamlit native secrets (`st.secrets`) over traditional `.env` environment variables.

## ADDED Requirements

### Requirement: Streamlit Secrets Priority

The system SHALL retrieve application configuration settings and API endpoints (such as `XANO_API_BASE`, `XANO_AUTH_API_BASE`, `XANO_ACADEMIC_API_BASE`, and `XANO_SUBJECT_API_BASE`) primarily from `st.secrets`.

#### Scenario: Reading configuration from st.secrets
- **WHEN** a configuration key is defined in `.streamlit/secrets.toml`
- **THEN** the system SHALL load the value from `st.secrets` without requiring `.env`.

#### Scenario: Fallback when running outside Streamlit context
- **WHEN** code is executed in an environment where `st.secrets` is unavailable or the key is not in `st.secrets`
- **THEN** the system SHALL fallback to `os.getenv()` or the provided default value.

### Requirement: Secrets File Protection

The system SHALL keep `.streamlit/secrets.toml` excluded from version control in `.gitignore`.

#### Scenario: Gitignore validation
- **WHEN** reviewing `.gitignore`
- **THEN** `.streamlit/` or `.streamlit/secrets.toml` MUST be present to prevent secret leakage.
