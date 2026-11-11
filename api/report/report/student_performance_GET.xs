// Retorna os dados consolidados de desempenho acadêmico do aluno autenticado
query "report/student-performance" verb=GET {
  api_group = "report"
  auth = "user"

  input {
  }

  stack {
    // 1. Busca todas as disciplinas vinculadas ao usuário autenticado
    db.query subjects {
      where  = ($db.subjects.user_id == $auth.id)
      return = {type: "list"}
    } as $subjects

    // 2. Busca todas as tarefas acadêmicas vinculadas ao usuário autenticado
    db.query academic_tasks {
      where  = ($db.academic_tasks.user_id == $auth.id)
      return = {type: "list"}
    } as $tasks

    // 3. Busca dados do usuário autenticado para identificação no relatório
    db.get user {
      field_name  = "id"
      field_value = $auth.id
      output      = ["id", "nome", "email"]
    } as $user
  }

  response = {
    user    : $user
    subjects: $subjects
    tasks   : $tasks
  }

  guid = "rpt-student-performance-get-001"
}
