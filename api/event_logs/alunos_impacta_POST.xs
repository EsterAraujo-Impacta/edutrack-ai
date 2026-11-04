// Add Alunos Impacta record
query alunos_impacta verb=POST {
  api_group = "Event Logs"

  input {
    dblink {
      table = ""
    }
  }

  stack {
    db.add "" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $alunos_impacta
  }

  response = $alunos_impacta
  guid = "6DrUZW9LetPPy2TPIqklNP6CIIQ"
}