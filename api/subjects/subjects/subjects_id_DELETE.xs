// Delete an academic subject owned by the authenticated user
query "subjects/{subjects_id}" verb=DELETE {
  api_group = "subjects"
  auth = ""

  input {
    int subjects_id filters=min:1
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
      error = "You do not have permission to delete this subject."
    }

    db.del subjects {
      field_name = "id"
      field_value = $input.subjects_id
    }
  }

  response = null
  guid = "PojQXq8kB-tPsOiQetwaAF-pTnw"
}

