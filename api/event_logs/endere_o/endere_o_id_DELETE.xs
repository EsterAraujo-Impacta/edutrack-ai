// Delete Endereço record.
query "endere_o/{endere_o_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int endere_o_id? filters=min:1
  }

  stack {
    db.del "" {
      field_name = "id"
      field_value = $input.endere_o_id
    }
  }

  response = null
  guid = "VAesuy1C6cTy0nS4yYYa_8l7e2g"
}