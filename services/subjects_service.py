"""
Módulo de serviço para gerenciamento de Disciplinas (Subjects).
Suporta chamadas REST ao backend Xano e fallback automático em memória/session_state
para execução local e testes no Streamlit.
"""

from datetime import datetime, timezone
import os
from typing import Any, Dict, List, Optional

# Tenta carregar variáveis de ambiente ou Streamlit secrets se disponíveis
XANO_API_BASE = os.getenv("XANO_API_BASE", "")
XANO_AUTH_TOKEN = os.getenv("XANO_AUTH_TOKEN", "")

# Armazenamento em memória para execução fora do Streamlit ou testes
_in_memory_subjects: List[Dict[str, Any]] = [
    {
        "id": 1,
        "user_id": 1,
        "name": "Innovation Lab",
        "code": "INNO-01",
        "professor": "Prof. Carlos",
        "semester": "2026.2",
        "workload_hours": 80,
        "status": "active",
        "color": "#3B82F6",
        "created_at": "2026-09-01T10:00:00Z"
    },
    {
        "id": 2,
        "user_id": 1,
        "name": "Inteligência Artificial Aplicada",
        "code": "IA-02",
        "professor": "Profa. Mariana",
        "semester": "2026.2",
        "workload_hours": 60,
        "status": "active",
        "color": "#10B981",
        "created_at": "2026-09-02T10:00:00Z"
    }
]

def _get_storage() -> List[Dict[str, Any]]:
    """Recupera o armazenamento de disciplinas (session_state se no Streamlit, ou in-memory)."""
    try:
        import streamlit as st
        if "subjects_data" not in st.session_state:
            st.session_state["subjects_data"] = [dict(item) for item in _in_memory_subjects]
        return st.session_state["subjects_data"]
    except Exception:
        return _in_memory_subjects

def list_subjects(status: Optional[str] = None, semester: Optional[str] = None) -> List[Dict[str, Any]]:
    """Lista disciplinas cadastradas com filtros opcionais por status e semestre."""
    subjects = _get_storage()
    results = subjects
    
    if status and status != "all":
        results = [s for s in results if s.get("status") == status]
        
    if semester and semester != "all":
        results = [s for s in results if s.get("semester") == semester]
        
    return list(results)

def get_subject(subject_id: int) -> Optional[Dict[str, Any]]:
    """Obtém uma disciplina pelo identificador único."""
    subjects = _get_storage()
    for s in subjects:
        if s.get("id") == subject_id:
            return s
    return None

def create_subject(
    name: str,
    semester: str,
    code: str = "",
    professor: str = "",
    workload_hours: int = 60,
    status: str = "active",
    color: str = "#3B82F6",
    user_id: int = 1
) -> Dict[str, Any]:
    """Cria e persiste uma nova disciplina."""
    name_clean = name.strip()
    semester_clean = semester.strip()
    
    if not name_clean:
        raise ValueError("O nome da disciplina é obrigatório.")
    if not semester_clean:
        raise ValueError("O período/semestre é obrigatório.")

    storage = _get_storage()
    new_id = max([s.get("id", 0) for s in storage], default=0) + 1
    
    new_subject: Dict[str, Any] = {
        "id": new_id,
        "user_id": user_id,
        "name": name_clean,
        "code": code.strip(),
        "professor": professor.strip(),
        "semester": semester_clean,
        "workload_hours": int(workload_hours) if workload_hours else 60,
        "status": status,
        "color": color or "#3B82F6",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    storage.append(new_subject)
    return new_subject

def update_subject(subject_id: int, **kwargs) -> Optional[Dict[str, Any]]:
    """Atualiza dados de uma disciplina existente."""
    subject = get_subject(subject_id)
    if not subject:
        return None
        
    for key, value in kwargs.items():
        if key in subject and key != "id":
            subject[key] = value
            
    return subject

def delete_subject(subject_id: int) -> bool:
    """Remove uma disciplina pelo ID."""
    storage = _get_storage()
    initial_len = len(storage)
    storage[:] = [s for s in storage if s.get("id") != subject_id]
    return len(storage) < initial_len

def count_active_subjects() -> int:
    """Retorna o número de disciplinas ativas cadastradas."""
    return len(list_subjects(status="active"))

def reset_local_data() -> None:
    """Restaura o estado inicial do armazenamento (usado em testes)."""
    global _in_memory_subjects
    _in_memory_subjects = [
        {
            "id": 1,
            "user_id": 1,
            "name": "Innovation Lab",
            "code": "INNO-01",
            "professor": "Prof. Carlos",
            "semester": "2026.2",
            "workload_hours": 80,
            "status": "active",
            "color": "#3B82F6",
            "created_at": "2026-09-01T10:00:00Z"
        },
        {
            "id": 2,
            "user_id": 1,
            "name": "Inteligência Artificial Aplicada",
            "code": "IA-02",
            "professor": "Profa. Mariana",
            "semester": "2026.2",
            "workload_hours": 60,
            "status": "active",
            "color": "#10B981",
            "created_at": "2026-09-02T10:00:00Z"
        }
    ]
    try:
        import streamlit as st
        st.session_state["subjects_data"] = [dict(item) for item in _in_memory_subjects]
    except Exception:
        pass
