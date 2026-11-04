// Update an existing academic subject owned by the authenticated user
query "subjects/{subjects_id}" verb=PATCH {
  api_group = "subjects"

  input {
    int subjects_id filters=min:1
    text name? filters=trim
    text teacher? filters=trim
    int hours? filters=min:0
  }

  stack {
    // Retrieve target subject
    db.get subjects {
      field_name = "id"
      field_value = $input.subjects_id
    } as $subject
  
    // Verify subject exists
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }
  
    // Ensure subject belongs to the authenticated user
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "You do not have permission to modify this subject."
    }
  
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch subjects {
      field_name = "id"
      field_value = $input.subjects_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $updated_subject
  }

  response = $updated_subject
  guid = "wFk8I70sy23M5mJwScSgZ6D2euc"
}