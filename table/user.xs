table user {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "wvsfR35zIX7vQHt6uYdMAIPuXM0"
}