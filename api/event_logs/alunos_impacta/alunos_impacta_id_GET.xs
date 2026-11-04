// Get Alunos Impacta record
query "alunos_impacta/{alunos_impacta_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int alunos_impacta_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.alunos_impacta_id
    } as $alunos_impacta
  
    precondition ($alunos_impacta != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $alunos_impacta
  guid = "lEsWJ8OGINVsJzOyGzOqkncKQMI"
}