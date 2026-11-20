"""scripts/spaced_repetition.py – Implementação do algoritmo SuperMemo-2 (SM-2)."""

from datetime import date, timedelta


def calculate_sm2(
    interval: int,
    repetitions: int,
    ease_factor: float,
    grade: int,
    today: date | None = None,
) -> dict:
  """Recalcula o agendamento de um flashcard baseado na nota (0 a 3).

  Notas:
    0 = Errou
    1 = Difícil
    2 = Bom
    3 = Fácil
  """
  if grade not in (0, 1, 2, 3):
    raise ValueError("A nota deve ser um inteiro entre 0 e 3.")

  current_date = today or date.today()
  current_interval = int(interval or 0)
  current_reps = int(repetitions or 0)
  current_ef = float(ease_factor or 2.5)

  if grade == 0:
    new_reps = 0
    new_interval = 1
    new_ef = current_ef
  else:
    if current_reps == 0:
      new_interval = 1
    elif current_reps == 1:
      new_interval = 6
    else:
      new_interval = round(current_interval * current_ef)

    new_reps = current_reps + 1
    new_ef = current_ef + (0.1 - (3 - grade) * (0.08 + (3 - grade) * 0.02))
    if new_ef < 1.3:
      new_ef = 1.3

  next_review_date = current_date + timedelta(days=new_interval)

  return {
      "interval": new_interval,
      "repetitions": new_reps,
      "ease_factor": round(new_ef, 2),
      "next_review": next_review_date.strftime("%Y-%m-%d"),
  }


def preview_intervals(
    interval: int, repetitions: int, ease_factor: float
) -> dict[int, int]:
  """Retorna um dicionário {nota: dias_ate_proxima_revisao} para exibir nos botões."""
  return {
      grade: calculate_sm2(interval, repetitions, ease_factor, grade)["interval"]
      for grade in (0, 1, 2, 3)
  }