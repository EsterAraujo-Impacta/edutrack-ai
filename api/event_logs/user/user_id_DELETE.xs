// Delete user record.
query "user/{user_id}" verb=DELETE {
  api_group = "Event Logs"

  input {
    int user_id? filters=min:1
  }

  stack {
    db.del user {
      field_name = "id"
      field_value = $input.user_id
    }
  }

  response = null
  guid = "2PZ5L8vhEryCARVMKWv7j1wXRZY"
}