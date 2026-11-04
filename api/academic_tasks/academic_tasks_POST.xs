// Add a new academic task for the authenticated user
query academic_tasks verb=POST {
  api_group = "academic_tasks"

  input {
    // Subject identifier to which the task belongs
    int subject_id filters=min:1
  
    // Title of the task
    text title filters=trim
  
    // Detailed description of the task
    text description? filters=trim
  
    // Due date for submission or completion
    date due_date
  
    // Task status (pending, completed, overdue)
    text status?=pending filters=trim
  }

  stack {
    // Verify that the specified subject exists and belongs to the authenticated user
    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject
  
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }
  
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "The specified subject does not belong to the authenticated user."
    }
  
    db.add academic_tasks {
      data = {
        user_id    : $auth.id
        subject_id : $input.subject_id
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : ($input.status != null ? $input.status : "pending")
        created_at : "now"
      }
    } as $task
  }

  response = $task
  guid = "YbRhGRFiaFr_OP9UuHQGbv6NLl8"
}