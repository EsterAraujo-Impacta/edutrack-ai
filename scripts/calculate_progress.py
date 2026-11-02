#!/usr/bin/env python3
"""
Módulo de cálculo de progresso acadêmico para o EduTrack AI.
Calcula a porcentagem de tarefas concluídas em relação ao total para uma disciplina
e retorna os dados estruturados em formato JSON.
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional
import urllib.error
import urllib.request

XANO_API_BASE = os.getenv("XANO_API_BASE", "")
XANO_TOKEN = os.getenv("XANO_TOKEN", "") or os.getenv("XANO_AUTH_TOKEN", "")


def fetch_tasks_for_subject(
    subject_id: int,
    api_base: Optional[str] = None,
    auth_token: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Consulta tarefas acadêmicas vinculadas ao usuário autenticado no backend CRUD.
    Filtra pela disciplina especificada via query parameter ou pós-processamento.
    Inclui o cabeçalho Authorization: Bearer <token> se informado via auth_token,
    parâmetro --token ou variável de ambiente XANO_TOKEN / XANO_AUTH_TOKEN.
    """
    base_url = (api_base or os.getenv("XANO_API_BASE", "") or XANO_API_BASE).rstrip("/")
    token = auth_token or os.getenv("XANO_TOKEN", "") or os.getenv("XANO_AUTH_TOKEN", "") or XANO_TOKEN

    if not base_url:
        raise ValueError(
            "URL base da API (XANO_API_BASE) não configurada. "
            "Defina a variável de ambiente XANO_API_BASE ou passe o parâmetro api_base."
        )

    endpoint_url = f"{base_url}/academic_tasks"
    if subject_id:
        endpoint_url = f"{endpoint_url}?subject_id={subject_id}"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(endpoint_url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status != 200:
                raise RuntimeError(f"Erro na API CRUD: HTTP {response.status}")
            data = json.loads(response.read().decode("utf-8"))
            if isinstance(data, list):
                return [t for t in data if t.get("subject_id") == subject_id]
            return []
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Falha ao consultar tarefas (HTTP {e.code}): {error_msg}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Erro de conexão com o endpoint {endpoint_url}: {e.reason}")


def calculate_subject_progress(
    subject_id: int,
    tasks: Optional[List[Dict[str, Any]]] = None,
    api_base: Optional[str] = None,
    auth_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calcula o progresso de uma disciplina com base na proporção de tarefas concluídas.

    Retorna um dicionário com:
        - subject_id (int): Identificador da disciplina
        - total_tasks (int): Quantidade total de tarefas
        - completed_tasks (int): Quantidade de tarefas concluídas
        - progress_percentage (float): Porcentagem de conclusão (0.0 a 100.0)
        - status (str): 'no_tasks', 'not_started', 'in_progress' ou 'completed'
    """
    if subject_id <= 0:
        raise ValueError("O ID da disciplina deve ser um inteiro positivo.")

    # Se a lista de tarefas não foi fornecida diretamente, consulta o endpoint CRUD
    if tasks is None:
        tasks = fetch_tasks_for_subject(
            subject_id=subject_id,
            api_base=api_base,
            auth_token=auth_token
        )

    # Garante filtragem correta pela disciplina
    subject_tasks = [t for t in tasks if t.get("subject_id") == subject_id] if tasks else []
    total_tasks = len(subject_tasks)

    if total_tasks == 0:
        return {
            "subject_id": subject_id,
            "total_tasks": 0,
            "completed_tasks": 0,
            "progress_percentage": 0.0,
            "status": "no_tasks"
        }

    # Critérios de status de tarefa concluída
    completed_statuses = {"completed", "concluida", "concluída", "done"}
    completed_tasks = sum(
        1 for t in subject_tasks
        if str(t.get("status", "")).strip().lower() in completed_statuses
    )

    percentage = round((completed_tasks / total_tasks) * 100, 2)

    if percentage == 100.0:
        status_label = "completed"
    elif percentage == 0.0:
        status_label = "not_started"
    else:
        status_label = "in_progress"

    return {
        "subject_id": subject_id,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "progress_percentage": percentage,
        "status": status_label
    }


def calculate_progress_json(
    subject_id: int,
    tasks: Optional[List[Dict[str, Any]]] = None,
    api_base: Optional[str] = None,
    auth_token: Optional[str] = None,
    indent: int = 2
) -> str:
    """
    Calcula o progresso e retorna o payload serializado como string JSON formatada.
    """
    progress_dict = calculate_subject_progress(
        subject_id=subject_id,
        tasks=tasks,
        api_base=api_base,
        auth_token=auth_token
    )
    return json.dumps(progress_dict, indent=indent, ensure_ascii=False)


def main() -> None:
    """Interface de linha de comando para o cálculo de progresso."""
    parser = argparse.ArgumentParser(
        description="Calcula o progresso de uma disciplina baseado nas tarefas acadêmicas."
    )
    parser.add_argument(
        "--subject-id",
        type=int,
        required=True,
        help="ID numérico da disciplina."
    )
    parser.add_argument(
        "--api-base",
        type=str,
        default=None,
        help="URL base da API Xano (opcional, fallback para env XANO_API_BASE)."
    )
    parser.add_argument(
        "--token",
        type=str,
        default=None,
        help="Token de autenticação JWT (opcional, fallback para env XANO_TOKEN ou XANO_AUTH_TOKEN)."
    )
    parser.add_argument(
        "--mock-tasks",
        type=str,
        default=None,
        help="Caminho para arquivo JSON contendo lista de tarefas para teste local offline."
    )

    args = parser.parse_args()

    tasks_data = None
    if args.mock_tasks:
        with open(args.mock_tasks, "r", encoding="utf-8") as f:
            tasks_data = json.load(f)

    try:
        output_json = calculate_progress_json(
            subject_id=args.subject_id,
            tasks=tasks_data,
            api_base=args.api_base,
            auth_token=args.token
        )
        print(output_json)
    except Exception as err:
        error_payload = {
            "error": True,
            "message": str(err),
            "subject_id": args.subject_id
        }
        print(json.dumps(error_payload, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

