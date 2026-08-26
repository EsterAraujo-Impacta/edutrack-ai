// Query all teste records
query teste verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $teste
  }

  response = $teste
}