"""auth_helper.py – Helpers HTTP reutilizáveis para os endpoints Xano.

Prioriza a leitura de configurações e URLs a partir de `st.secrets` (Streamlit).
Caso executado fora do contexto do Streamlit ou na ausência da chave,
faz fallback seguro para variáveis de ambiente via `os.getenv()` / .env.
"""

import os
import json
import urllib.request
from urllib.error import HTTPError, URLError
from pathlib import Path


def get_config(key: str, default: str = "") -> str:
    """Recupera um parâmetro de configuração com prioridade:
    1. st.secrets (Streamlit Secrets nativo)
    2. os.getenv() (Variáveis de ambiente do sistema / .env)
    3. default
    """
    try:
        import streamlit as st
        if key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass

    # Fallback para .env caso disponível e chave não definida no ambiente
    val = os.getenv(key)
    if val is not None and val != "":
        return val

    try:
        from dotenv import load_dotenv
        _env_path = Path(__file__).resolve().parent.parent / ".env"
        if _env_path.exists():
            load_dotenv(dotenv_path=_env_path)
            val = os.getenv(key)
            if val is not None and val != "":
                return val
    except Exception:
        pass

    return default


def get_xano_api_base() -> str:
    """Retorna a URL base do Xano configurada."""
    base = get_config("XANO_API_BASE", "")
    if not base:
        base = get_config("XANO_AUTH_API_BASE", "")
    if not base:
        raise RuntimeError(
            "XANO_API_BASE não está definido em st.secrets nem no ambiente. "
            "Configure em .streamlit/secrets.toml com: XANO_API_BASE = 'https://<instancia>.xano.io/api'"
        )
    return base


# Compatibilidade retroativa para importações de XANO_API_BASE
try:
    XANO_API_BASE: str = get_xano_api_base()
except Exception:
    XANO_API_BASE: str = ""


def _request(
    method: str,
    endpoint: str,
    data: dict | None = None,
    token: str | None = None,
    base_url: str | None = None,
) -> dict:
    """Executa uma requisição HTTP para um endpoint Xano.

    Args:
        method:   "GET" ou "POST".
        endpoint: Caminho relativo à URL base (ex.: "/auth/login").
        data:     Payload JSON para requisições POST.
        token:    JWT para o cabeçalho Authorization (opcional).
        base_url: URL base personalizada (opcional, fallback para XANO_API_BASE).

    Returns:
        Resposta JSON parseada como dict/list Python.

    Raises:
        RuntimeError: em caso de erro HTTP ou de rede.
    """
    resolved_base = (base_url or get_xano_api_base()).rstrip("/")
    url = f"{resolved_base}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    encoded_data = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method.upper())

    try:
        with urllib.request.urlopen(req) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return json.loads(resp.read().decode(charset))
    except HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            msg = json.loads(body).get("message", body)
        except Exception:
            msg = body
        raise RuntimeError(f"Erro HTTP {exc.code}: {msg}") from None
    except URLError as exc:
        raise RuntimeError(f"Erro de rede: {exc.reason}") from None


def post(endpoint: str, payload: dict, token: str | None = None, base_url: str | None = None) -> dict:
    """Atalho para requisições POST."""
    return _request("POST", endpoint, data=payload, token=token, base_url=base_url)


def get(endpoint: str, token: str, base_url: str | None = None) -> dict:
    """Atalho para requisições GET autenticadas."""
    return _request("GET", endpoint, token=token, base_url=base_url)
