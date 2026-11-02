// List all academic subjects belonging to the authenticated user
query subjects verb=GET {
  api_group = "subjects"
  auth = ""

  input {
  }

  stack {
    db.query subjects {
      where = ($db.subjects.user_id == $auth.id)
      return = {type: "list"}
    } as $subjects
  }

  response = $subjects
  guid = "wgHy2LM9SO9NZPk2Dj1cOJdk7q4"
}

