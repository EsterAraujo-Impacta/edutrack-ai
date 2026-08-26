// Query all Endereço records
query endere_o verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $endere_o
  }

  response = $endere_o
}