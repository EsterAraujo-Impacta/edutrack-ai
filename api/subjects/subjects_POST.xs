// Add a new academic subject for the authenticated user
query subjects verb=POST {
  api_group = "subjects"
  auth = ""

  input {
    // Subject name
    text name filters=trim

    // Responsible teacher
    text teacher? filters=trim

    // Workload in hours
    int hours? filters=min:0
  }

  stack {
    db.add subjects {
      data = {
        name: $input.name
        teacher: $input.teacher
        hours: $input.hours
        user_id: $auth.id
        created_at: "now"
      }
    } as $subject
  }

  response = $subject
  guid = "7LyMzzf5Q3-JXgmAK-FpVwVgLo4"
}

