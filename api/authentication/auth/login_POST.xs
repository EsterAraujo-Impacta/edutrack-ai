// Login e retorno de token de autenticação
query "auth/login" verb=POST {
  api_group = "Authentication"

  input {
    email email? filters=trim|lower
    text senha?
  }

  stack {
    db.get user {
      field_name = "email"
      field_value = $input.email
      output = ["id", "created_at", "nome", "email", "senha"]
    } as $user

    precondition ($user != null) {
      error = "Invalid Credentials."
    }

    security.check_password {
      text_password = $input.senha
      hash_password = $user.senha
    } as $pass_result

    precondition ($pass_result) {
      error = "Invalid Credentials."
    }

    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $authToken
  }

  response = {authToken: $authToken}
  guid = "1SU5qF7TKq9Krl3WSXaYpsmTtuM"
}