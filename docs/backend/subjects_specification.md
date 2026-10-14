# Especificação de Backend: Disciplinas (Subjects)

Este documento define o esquema da tabela no Xano e o contrato dos endpoints REST para o gerenciamento de disciplinas no EduTrack AI.

---

## 1. Schema da Tabela: `subjects`

| Campo | Tipo | Nulo | Padrão | Descrição |
| :--- | :--- | :---: | :---: | :--- |
| `id` | `integer` (PK) | Não | Auto | Identificador único da disciplina |
| `created_at` | `timestamp` | Não | `now` | Data e hora de criação |
| `user_id` | `integer` | Não | - | Chave estrangeira referenciando o estudante (`user.id`) |
| `name` | `text` | Não | - | Nome da matéria (ex.: "Innovation Lab") |
| `code` | `text` | Sim | `null` | Código ou sigla da matéria (ex.: "INNO-01") |
| `professor` | `text` | Sim | `null` | Nome do professor(a) responsável |
| `semester` | `text` | Não | - | Período ou semestre letivo (ex.: "2026.2") |
| `workload_hours` | `integer` | Sim | `60` | Carga horária total em horas |
| `status` | `text` | Não | `'active'` | Status da matéria: `'active'`, `'completed'`, `'dropped'` |
| `color` | `text` | Sim | `'#3B82F6'` | Cor em hexadecimal para exibição visual |

### Índices recomendados:
- Índice em `user_id` para busca eficiente por estudante.
- Índice composto em `(user_id, status)` para filtros rápidos.

---

## 2. Contratos da API (`/subjects`)

### 2.1 `GET /subjects`
Lista todas as disciplinas do estudante autenticado.
- **Autenticação**: Obrigatória (Bearer Token)
- **Query Params**:
  - `status` (opcional): `'active'`, `'completed'`, `'dropped'`
  - `semester` (opcional): ex.: `'2026.2'`
- **Resposta Sucesso (200 OK)**:
```json
[
  {
    "id": 1,
    "user_id": 42,
    "name": "Innovation Lab",
    "code": "INNO-01",
    "professor": "Prof. Carlos",
    "semester": "2026.2",
    "workload_hours": 80,
    "status": "active",
    "color": "#3B82F6",
    "created_at": 1727092800000
  }
]
```

---

### 2.2 `POST /subjects`
Cria uma nova disciplina vinculada ao estudante autenticado.
- **Autenticação**: Obrigatória (Bearer Token)
- **Body (JSON)**:
```json
{
  "name": "Innovation Lab",
  "code": "INNO-01",
  "professor": "Prof. Carlos",
  "semester": "2026.2",
  "workload_hours": 80,
  "status": "active",
  "color": "#3B82F6"
}
```
- **Campos Obrigatórios**: `name`, `semester`
- **Resposta Sucesso (201 Created)**: Objeto da disciplina criada.

---

### 2.3 `GET /subjects/{id}`
Obtém os detalhes de uma disciplina específica pelo ID.
- **Autenticação**: Obrigatória (Bearer Token)
- **Resposta Sucesso (200 OK)**: Objeto da disciplina.
- **Erro (404 Not Found)**: Caso a disciplina não pertença ao usuário ou não exista.

---

### 2.4 `PUT /subjects/{id}`
Atualiza os dados de uma disciplina existente.
- **Autenticação**: Obrigatória (Bearer Token)
- **Body (JSON)**: Campos a serem alterados.
- **Resposta Sucesso (200 OK)**: Objeto atualizado da disciplina.

---

### 2.5 `DELETE /subjects/{id}`
Remove uma disciplina.
- **Autenticação**: Obrigatória (Bearer Token)
- **Resposta Sucesso (200 OK)**:
```json
{
  "success": true,
  "message": "Disciplina removida com sucesso."
}
```
