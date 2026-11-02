// Update an existing academic task owned by the authenticated user
query "academic_tasks/{academic_tasks_id}" verb=PATCH {
  api_group = "academic_tasks"
  auth = ""

  input {
    int academic_tasks_id filters=min:1
    int subject_id? filters=min:1
    text title? filters=trim
    text description? filters=trim
    date due_date?
    text status? filters=trim
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
      error = "You do not have permission to modify this academic task."
    }

    // If subject_id is being updated, verify that the target subject belongs to the authenticated user
    conditional {
      if ($input.subject_id != null) {
        db.get subjects {
          field_name = "id"
          field_value = $input.subject_id
        } as $subject

        conditional {
          if ($subject == null) {
            throw {
              name = "notfound"
              value = "Subject not found."
            }
          }
        }

        conditional {
          if ($subject.user_id != $auth.id) {
            throw {
              name = "accessdenied"
              value = "The specified subject does not belong to the authenticated user."
            }
          }
        }
      }
    }

    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input

    db.patch academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $updated_task
  }

  response = $updated_task
  guid = "reshfz1QmyTVn4f5W4JZsD16yEc"
}
