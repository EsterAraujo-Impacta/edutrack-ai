"""auth_helper.py – Helpers HTTP reutilizáveis para os endpoints Xano.

Carrega XANO_API_BASE do arquivo .env na raiz do projeto (via python-dotenv).
Injeta o cabeçalho ``Authorization: Bearer <token>`` automaticamente quando
um token é fornecido. Usa apenas stdlib (urllib.request) + python-dotenv.
"""

import os
import json
import urllib.request
from urllib.error import HTTPError, URLError
from pathlib import Path
from dotenv import load_dotenv

# Resolve o .env na raiz do projeto (pages/ → ../)
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)

XANO_API_BASE: str = os.getenv("XANO_API_BASE", "")
if not XANO_API_BASE:
    raise RuntimeError(
        "XANO_API_BASE não está definido. "
        "Crie o arquivo .env na raiz do projeto com: XANO_API_BASE=https://<instancia>.xano.io/api"
    )


def _request(
    method: str,
    endpoint: str,
    data: dict | None = None,
    token: str | None = None,
) -> dict:
    """Executa uma requisição HTTP para um endpoint Xano.

    Args:
        method:   "GET" ou "POST".
        endpoint: Caminho relativo à XANO_API_BASE (ex.: "/auth/login").
        data:     Payload JSON para requisições POST.
        token:    JWT para o cabeçalho Authorization (opcional).

    Returns:
        Resposta JSON parseada como dict/list Python.

    Raises:
        RuntimeError: em caso de erro HTTP ou de rede.
    """
    url = f"{XANO_API_BASE.rstrip('/')}{endpoint}"
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


def post(endpoint: str, payload: dict, token: str | None = None) -> dict:
    """Atalho para requisições POST."""
    return _request("POST", endpoint, data=payload, token=token)


def get(endpoint: str, token: str) -> dict:
    """Atalho para requisições GET autenticadas."""
    return _request("GET", endpoint, token=token)

