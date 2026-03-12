# Sequence Flow: Application Search

- sequence_id: SEQ-001
- requirement_ids:
  - REQ-001

```mermaid
sequenceDiagram
    participant User
    participant UI
    participant API
    User->>UI: Enter search conditions
    UI->>API: Request search
    API-->>UI: Return results
    UI-->>User: Render search results
```
