// Delete Alunos Impacta record.
query "alunos_impacta/{alunos_impacta_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int alunos_impacta_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.alunos_impacta_id
    }
  }

  response = null
  guid = "WIlab7AjoG3TDNrhENadwCLzyTI"
}