// Query all Alunos Impacta records
query alunos_impacta verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $alunos_impacta
  }

  response = $alunos_impacta
}