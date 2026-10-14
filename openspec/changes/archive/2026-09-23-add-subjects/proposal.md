# Change: feature-notas-atividades

# Proposal

## Why

Atualmente, o EduTrack AI possui apenas um protótipo estático no Streamlit e uma estrutura inicial no Xano, sem suporte a cadastro e gerenciamento de disciplinas acadêmicas ("Minhas Disciplinas"). A adição do módulo de disciplinas é o alicerce fundamental para que os estudantes possam estruturar seus cursos, registrar professores, acompanhar status e associar tarefas e notas a cada matéria.

## What Changes

- Introdução da entidade e capacidade de disciplinas (`subjects`) no sistema.
- Definição dos campos principais: nome, código da disciplina, professor, período/semestre, carga horária, status (ativa/concluída/trancada) e cor de identificação.
- Criação dos endpoints de API no backend (Xano) para CRUD completo de disciplinas (listar, criar, atualizar e excluir).
- Integração da aba "Disciplinas" no Streamlit (`app.py`), substituindo o placeholder por formulário de cadastro e listagem dinâmica.
- Conexão da métrica "Disciplinas Ativas" no Dashboard do Streamlit.

## Capabilities

### New Capabilities
- `subjects`: Gerenciamento completo do ciclo de vida de disciplinas acadêmicas (cadastro, consulta, edição e exclusão), com metadados do semestre e status.

### Modified Capabilities

## Impact

- **Backend (Xano)**: Nova tabela `subjects` e API group `subjects` com endpoints REST protegidos.
- **Frontend (Streamlit)**: Modificação em `app.py` para integração com os dados de disciplinas e exibição dinâmica.
- **APIs e Modelos**: Nova estrutura de dados no sistema com chave primária e vínculo ao estudante.
