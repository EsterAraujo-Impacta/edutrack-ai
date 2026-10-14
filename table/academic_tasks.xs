table academic_tasks {
  auth = false

  schema {
    // Identificador único da tarefa acadêmica
    int id
  
    // FK para o estudante dono da tarefa
    int user_id {
      table = "user"
    }
  
    // FK para a disciplina correspondente
    int subject_id {
      table = "subjects"
    }
  
    // Título da tarefa ou obrigação acadêmica
    text title
  
    // Descrição detalhada ou instruções da tarefa
    text description?
  
    // Data limite de entrega ou realização
    date due_date
  
    // Status da tarefa (ex: pending, completed, overdue)
    text status?=pending
  
    // Data de registro da tarefa no sistema
    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {
      type : "btree"
      field: [{name: "user_id"}, {name: "subject_id"}]
    }
  ]

  guid = "gM7evLhtswYAe5pNAgmkjnqB4f0"
}