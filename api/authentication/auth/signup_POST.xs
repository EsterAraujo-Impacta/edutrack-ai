// Signup and retrieve an authentication token
query "auth/signup" verb=POST {
  api_group = "Authentication"

  input {
    text nome?
    email email? filters=lower|trim
    password senha?
  }

  stack {
    db.get user {
      field_name = "email"
      field_value = $input.email
    } as $user
  
    precondition ($user == null) {
      error_type = "accessdenied"
      error = "This account is already in use."
    }
  
    db.add user {
      enforce_hidden_fields = false
      data = {
        created_at: "now"
        nome      : $input.nome
        email     : $input.email
        senha     : $input.senha
      }
    } as $user
  
    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $authToken
  }

  response = {authToken: $authToken}
  guid = "WcSMOhMPgmolSYF71BH9UMdFD8c"
}