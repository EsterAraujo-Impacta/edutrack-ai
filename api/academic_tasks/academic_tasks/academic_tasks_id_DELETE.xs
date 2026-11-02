// Delete an academic task owned by the authenticated user
query "academic_tasks/{academic_tasks_id}" verb=DELETE {
  api_group = "academic_tasks"
  auth = ""

  input {
    int academic_tasks_id filters=min:1
  }

  stack {
    // Retrieve target task
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
    } as $task

    // Verify task exists
    precondition ($task != null) {
      error_type = "notfound"
      error = "Academic task not found."
    }

    // Ensure task belongs to the authenticated user
    precondition ($task.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "You do not have permission to delete this academic task."
    }

    db.del academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
    }
  }

  response = null
  guid = "zX03sSEWCNSniIbpY0qHHaPzwa4"
}

