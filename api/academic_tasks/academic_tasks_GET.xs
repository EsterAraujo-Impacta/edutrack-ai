// List all academic tasks belonging to the authenticated user
query academic_tasks verb=GET {
  api_group = "academic_tasks"

  input {
    // Optional filter by subject ID
    int subject_id? filters=min:1
  }

  stack {
    db.query academic_tasks {
      where = ($db.academic_tasks.user_id == $auth.id)
      return = {type: "list"}
    } as $tasks
  }

  response = $tasks
  guid = "EBtrf066ggVy-ljsJRerInn5rl8"
}