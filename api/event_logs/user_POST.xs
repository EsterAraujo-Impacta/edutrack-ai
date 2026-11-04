// Add user record
query user verb=POST {
  api_group = "Event Logs"

  input {
    dblink {
      table = "user"
    }
  }

  stack {
    db.add user {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $user
  }

  response = $user
  guid = "E-IjEm1ruiOhK4BMnS_T_MkAjgg"
}