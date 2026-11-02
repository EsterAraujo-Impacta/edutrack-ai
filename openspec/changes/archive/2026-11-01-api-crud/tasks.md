# Tasks

## 1. Endpoints CRUD para Subjects (Xano)

- [x] 1.1 Criar o arquivo de grupo de API `api/subjects/subjects.xs` definindo `api_group "subjects"` e verificar a declaração correta da estrutura
- [x] 1.2 Criar o endpoint `api/subjects/subjects_POST.xs` para cadastrar disciplina vinculada automaticamente a `$auth.id` e verificar associação do `user_id`
- [x] 1.3 Criar o endpoint `api/subjects/subjects_GET.xs` para listar disciplinas com filtro `user_id == $auth.id` e verificar que retorna apenas dados do usuário logado
- [x] 1.4 Criar o endpoint `api/subjects/subjects/subjects_id_PATCH.xs` para atualizar disciplina validando a propriedade por `$auth.id` e verificar bloqueio contra alterações indevidas
- [x] 1.5 Criar o endpoint `api/subjects/subjects/subjects_id_DELETE.xs` para remover disciplina validando a propriedade por `$auth.id` e verificar bloqueio contra exclusão de registros de terceiros

## 2. Endpoints CRUD para Academic Tasks (Xano)

- [x] 2.1 Criar o arquivo de grupo de API `api/academic_tasks/academic_tasks.xs` definindo `api_group "academic_tasks"` e verificar a declaração correta da estrutura
- [x] 2.2 Criar o endpoint `api/academic_tasks/academic_tasks_POST.xs` para cadastrar tarefa acadêmica vinculada automaticamente a `$auth.id` e verificar associação do `user_id`
- [x] 2.3 Criar o endpoint `api/academic_tasks/academic_tasks_GET.xs` para listar tarefas acadêmicas com filtro `user_id == $auth.id` e verificar que retorna apenas dados do usuário logado
- [x] 2.4 Criar o endpoint `api/academic_tasks/academic_tasks/academic_tasks_id_PATCH.xs` para atualizar tarefa acadêmica validando a propriedade por `$auth.id` e verificar bloqueio contra IDOR
- [x] 2.5 Criar o endpoint `api/academic_tasks/academic_tasks/academic_tasks_id_DELETE.xs` para remover tarefa acadêmica validando a propriedade por `$auth.id` e verificar bloqueio contra exclusão de registros de terceiros

