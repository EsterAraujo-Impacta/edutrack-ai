// Edit Alunos Impacta record
query "alunos_impacta/{alunos_impacta_id}" verb=PATCH {
  api_group = "Event Logs"

  input {
    int alunos_impacta_id? filters=min:1
    dblink {
      table = ""
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch "" {
      field_name = "id"
      field_value = $input.alunos_impacta_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $alunos_impacta
  }

  response = $alunos_impacta
}