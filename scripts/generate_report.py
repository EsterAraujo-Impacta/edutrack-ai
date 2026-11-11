#!/usr/bin/env python3
"""scripts/generate_report.py – Gerador de relatório PDF de desempenho acadêmico.

Coleta os dados do aluno (disciplinas e tarefas) no backend Xano, calcula as
métricas de progresso por disciplina e gera um documento PDF formatado
utilizando a biblioteca ReportLab.
"""

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional
import urllib.error
import urllib.request

# Carrega as variáveis do .env logo na inicialização
try:
  from dotenv import load_dotenv

  load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
except ImportError:
  pass

try:
  from reportlab.lib import colors
  from reportlab.lib.pagesizes import A4
  from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
  from reportlab.lib.units import cm
  from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
except ImportError:
  print(
      "ERRO: A biblioteca 'reportlab' não está instalada.\n"
      "Instale executando: pip install reportlab",
      file=sys.stderr,
  )
  sys.exit(1)

# Importa a função de cálculo de progresso existente para reutilização
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
  from calculate_progress import calculate_subject_progress
except ImportError:

  def calculate_subject_progress(
      subject_id: Any, tasks: Optional[List[Dict[str, Any]]] = None, **kwargs
  ) -> Dict[str, Any]:
    str_subject_id = str(subject_id).strip() if subject_id is not None else ""

    # Suporta diferentes estruturas de ID das tarefas no Xano
    subject_tasks = [
        t
        for t in (tasks or [])
        if str(
            t.get("subject_id")
            or t.get("subjects_id")
            or (
                t.get("subject", {}).get("id")
                if isinstance(t.get("subject"), dict)
                else t.get("subject")
            )
        ).strip()
        == str_subject_id
    ]

    total = len(subject_tasks)
    if total == 0:
      return {
          "subject_id": subject_id,
          "total_tasks": 0,
          "completed_tasks": 0,
          "progress_percentage": 0.0,
          "status": "Sem tarefas",
      }

    completed = sum(
        1
        for t in subject_tasks
        if str(t.get("status", "")).strip().lower()
        in {"completed", "concluida", "concluída", "done"}
    )
    pct = round((completed / total) * 100, 2)
    status_str = (
        "Concluído"
        if pct == 100.0
        else ("Não iniciado" if pct == 0.0 else "Em andamento")
    )

    return {
        "subject_id": subject_id,
        "total_tasks": total,
        "completed_tasks": completed,
        "progress_percentage": pct,
        "status": status_str,
    }


def _resolve_token(cli_token: Optional[str]) -> str:
  if cli_token:
    return cli_token
  for var_name in ("XANO_TOKEN", "XANO_AUTH_TOKEN"):
    val = os.getenv(var_name, "").strip()
    if val:
      return val
  token_file = Path(".auth_token")
  if token_file.exists():
    return token_file.read_text(encoding="utf-8").strip()
  return ""


def _resolve_api_base(cli_base: Optional[str]) -> str:
  if cli_base:
    return cli_base.rstrip("/")
  base = os.getenv("XANO_API_BASE", "").rstrip("/")
  if not base:
    base = os.getenv("XANO_AUTH_API_BASE", "").rstrip("/")
  if not base:
    raise ValueError(
        "URL base da API não configurada no .env (XANO_API_BASE ou"
        " XANO_AUTH_API_BASE)."
    )
  return base


def fetch_report_data(api_base: str, token: str) -> Dict[str, Any]:
  headers = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Authorization": f"Bearer {token}",
  }

  auth_base = os.getenv("XANO_AUTH_API_BASE", api_base).rstrip("/")
  academic_base = os.getenv("XANO_ACADEMIC_API_BASE", api_base).rstrip("/")
  subject_base = os.getenv("XANO_SUBJECT_API_BASE", api_base).rstrip("/")

  def _fetch(url: str) -> Any:
    print(f"Buscando: {url}")
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=15) as response:
      return json.loads(response.read().decode("utf-8"))

  user = _fetch(f"{auth_base}/auth/me")
  subjects = _fetch(f"{subject_base}/subjects")
  tasks = _fetch(f"{academic_base}/academic_tasks")

  return {
      "user": user if isinstance(user, dict) else {},
      "subjects": subjects if isinstance(subjects, list) else [],
      "tasks": tasks if isinstance(tasks, list) else [],
  }


def generate_pdf_report(
    report_data: Dict[str, Any],
    output_path: str,
) -> None:
  user = report_data.get("user") or {}
  subjects = report_data.get("subjects") or []
  tasks = report_data.get("tasks") or []

  user_name = user.get("nome") or user.get("name") or "Estudante"
  user_email = user.get("email") or "—"
  generated_at = datetime.now().strftime("%d/%m/%Y %H:%M")

  doc = SimpleDocTemplate(
      output_path,
      pagesize=A4,
      rightMargin=2 * cm,
      leftMargin=2 * cm,
      topMargin=2 * cm,
      bottomMargin=2 * cm,
  )

  styles = getSampleStyleSheet()
  title_style = ParagraphStyle(
      "DocTitle",
      parent=styles["Title"],
      fontSize=18,
      spaceAfter=6,
      textColor=colors.HexColor("#1e293b"),
  )
  sub_style = ParagraphStyle(
      "DocSubtitle",
      parent=styles["Normal"],
      fontSize=10,
      textColor=colors.HexColor("#475569"),
      spaceAfter=12,
  )
  subject_title_style = ParagraphStyle(
      "SubjectTitle",
      parent=styles["Heading2"],
      fontSize=12,
      textColor=colors.HexColor("#0f172a"),
      spaceBefore=12,
      spaceAfter=4,
  )

  story = []

  # Cabeçalho
  story.append(Paragraph("Relatório de Desempenho Acadêmico", title_style))
  story.append(
      Paragraph(
          f"Aluno: <b>{user_name}</b>  |  E-mail: {user_email}"
          f"  |  Gerado em: {generated_at}",
          sub_style,
      )
  )
  story.append(
      HRFlowable(
          width="100%",
          thickness=1,
          color=colors.HexColor("#0284c7"),
          spaceAfter=12,
      )
  )

  if not subjects:
    story.append(
        Paragraph(
            "Nenhuma disciplina cadastrada para este aluno.", styles["Normal"]
        )
    )
  else:
    for subj in sorted(
        subjects, key=lambda s: str(s.get("name") or s.get("nome") or "").lower()
    ):
      subj_id = subj.get("id")
      progress = calculate_subject_progress(subject_id=subj_id, tasks=tasks)

      # Mapeia os nomes das propriedades considerando variações em português/inglês
      subj_name = (
          subj.get("nome")
          or subj.get("name")
          or subj.get("subject_name")
          or "Disciplina sem nome"
      )
      teacher_name = (
          subj.get("professor")
          or subj.get("teacher")
          or subj.get("docente")
          or "Não informado"
      )
      hours = (
          subj.get("hours")
          or subj.get("carga_horaria")
          or subj.get("hours_count")
      )
      hours_str = f"{hours}h" if hours is not None else "—"

      story.append(Paragraph(f"📚 {subj_name}", subject_title_style))

      table_rows = [
          ["Professor(a)", str(teacher_name)],
          ["Carga Horária", hours_str],
          [
              "Tarefas Concluídas",
              f"{progress['completed_tasks']} de {progress['total_tasks']}",
          ],
          [
              "Progresso",
              f"{progress['progress_percentage']:.1f}% ({progress['status']})",
          ],
      ]

      table = Table(table_rows, colWidths=[5 * cm, 10 * cm])
      table.setStyle(
          TableStyle([
              ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f1f5f9")),
              ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#0f172a")),
              ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
              ("FONTSIZE", (0, 0), (-1, -1), 9),
              (
                  "ROWBACKGROUNDS",
                  (0, 0),
                  (-1, -1),
                  [colors.white, colors.HexColor("#f8fafc")],
              ),
              ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
              ("LEFTPADDING", (0, 0), (-1, -1), 8),
              ("RIGHTPADDING", (0, 0), (-1, -1), 8),
              ("TOPPADDING", (0, 0), (-1, -1), 5),
              ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
          ])
      )
      story.append(table)
      story.append(Spacer(1, 0.3 * cm))

  # Rodapé institucional
  story.append(Spacer(1, 0.8 * cm))
  story.append(
      HRFlowable(
          width="100%",
          thickness=0.5,
          color=colors.HexColor("#94a3b8"),
          spaceAfter=6,
      )
  )
  story.append(
      Paragraph(
          "<font size='8' color='#64748b'>EduTrack AI • Documento gerado"
          " automaticamente pelo sistema de gestão acadêmica.</font>",
          styles["Normal"],
      )
  )

  doc.build(story)


def main() -> None:
  parser = argparse.ArgumentParser(
      description=(
          "Gera relatório em PDF do desempenho acadêmico do aluno a partir dos"
          " dados do Xano."
      )
  )
  parser.add_argument(
      "--token", type=str, default=None, help="Token JWT de autenticação."
  )
  parser.add_argument(
      "--api-base", type=str, default=None, help="URL base da API Xano."
  )
  parser.add_argument(
      "--output",
      type=str,
      default="relatorio_desempenho.pdf",
      help=(
          "Caminho do arquivo PDF de saída (padrão: relatorio_desempenho.pdf)."
      ),
  )
  args = parser.parse_args()

  token = _resolve_token(args.token)
  if not token:
    print(
        "ERRO: Token JWT não fornecido via --token, variável de ambiente ou"
        " .auth_token.",
        file=sys.stderr,
    )
    sys.exit(1)

  try:
    api_base = _resolve_api_base(args.api_base)
    data = fetch_report_data(api_base=api_base, token=token)
    generate_pdf_report(report_data=data, output_path=args.output)
    print(f"Sucesso: Relatório PDF gerado em '{args.output}'.")
  except Exception as exc:
    print(f"ERRO: {exc}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
  main()