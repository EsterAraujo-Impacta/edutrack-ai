// Query all user records
query user verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query user {
      return = {type: "list"}
    } as $user
  }

  response = $user
  guid = "MEEJEgpy0IzFbZ6JkYF8TV2KJXY"
}