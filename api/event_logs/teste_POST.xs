// Add teste record
query teste verb=POST {
  api_group = "Event Logs"

  input {
    dblink {
      table = ""
    }
  }

  stack {
    db.add "" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $teste
  }

  response = $teste
  guid = "xk2wLaJfS64dOzg_VH3nDpvPiac"
}