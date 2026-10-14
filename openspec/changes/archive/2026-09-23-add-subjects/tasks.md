# Tasks

## 1. Modelo de Dados e Backend (Xano)

- [ ] 1.1 Definir a especificação da tabela `subjects` (campos: id, user_id, name, code, professor, semester, workload_hours, status, color) e verificar integridade dos tipos e obrigatoriedade
- [ ] 1.2 Definir e documentar os endpoints da API `/subjects` (GET /subjects, POST /subjects, PUT /subjects/{id}, DELETE /subjects/{id}) e verificar aderência aos requisitos da especificação
- [x] 1.1 Definir a especificação da tabela `subjects` (campos: id, user_id, name, code, professor, semester, workload_hours, status, color) e verificar integridade dos tipos e obrigatoriedade
- [x] 1.2 Definir e documentar os endpoints da API `/subjects` (GET /subjects, POST /subjects, PUT /subjects/{id}, DELETE /subjects/{id}) e verificar aderência aos requisitos da especificação

## 2. Camada de Serviço e Integração

- [ ] 2.1 Criar `services/subjects_service.py` implementando métodos CRUD com suporte a fallback de dados local (mock em session_state) e verificar execução de operações básicas
- [ ] 2.2 Criar testes unitários para o serviço de disciplinas e verificar execução com sucesso via pytest ou unittest
- [x] 2.1 Criar `services/subjects_service.py` implementando métodos CRUD com suporte a fallback de dados local (mock em session_state) e verificar execução de operações básicas
- [x] 2.2 Criar testes unitários para o serviço de disciplinas e verificar execução com sucesso via pytest ou unittest

## 3. Interface Streamlit (Frontend)

- [ ] 3.1 Construir formulário de cadastro de disciplinas na aba "Disciplinas" de `app.py` e verificar submissão com campos obrigatórios validados
- [ ] 3.2 Implementar listagem visual em cards das disciplinas cadastradas com filtros por status e semestre, verificando exibição correta dos dados
- [ ] 3.3 Conectar a métrica "Disciplinas Ativas" no Dashboard de `app.py` ao serviço de disciplinas e verificar exibição do total de disciplinas ativas
- [x] 3.1 Construir formulário de cadastro de disciplinas na aba "Disciplinas" de `app.py` e verificar submissão com campos obrigatórios validados
- [x] 3.2 Implementar listagem visual em cards das disciplinas cadastradas com filtros por status e semestre, verificando exibição correta dos dados
- [x] 3.3 Conectar a métrica "Disciplinas Ativas" no Dashboard de `app.py` ao serviço de disciplinas e verificar exibição do total de disciplinas ativas

## 4. Verificação de Ponta a Ponta

- [ ] 4.1 Testar fluxo completo no Streamlit (cadastrar disciplina, visualizar na lista e verificar incremento no Dashboard) e validar ausência de erros em tempo de execução
- [x] 4.1 Testar fluxo completo no Streamlit (cadastrar disciplina, visualizar na lista e verificar incremento no Dashboard) e validar ausência de erros em tempo de execução

