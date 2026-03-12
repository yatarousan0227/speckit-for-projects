# Glossary

This glossary defines shared domain terms and naming conventions for the ToDo application.

- Task:
  - A user-owned work item that has a title, optional description, status, and optional due date.
- Open Task:
  - A task that is not yet completed and is still actionable.
- Completed Task:
  - A task whose work is finished and whose status is persisted as completed.
- Archived Task:
  - A task hidden from the default working list but still retained for history or recovery.
- Due Date:
  - The target calendar date by which the task should be completed.
- Reminder:
  - A notification triggered before or on a task due date.
- Task List:
  - A collection view of tasks presented with filters, sorting, and summary counts.
- Filter:
  - A user-selected condition such as status, due date range, or keyword used to narrow visible tasks.
- Authenticated User:
  - The signed-in person who owns and manages their own tasks.
- Ownership Check:
  - The server-side verification that the acting user is allowed to read or change the target task.
- Soft Delete:
  - A logical deletion strategy where the record is hidden from normal use without immediate physical removal.

## Naming Conventions

- Use `task` for the singular domain object.
- Use `tasks` for collection-level routes, modules, and directories.
- Use `completedAt` for the timestamp when a task is completed.
- Use `dueDate` for the planned deadline field.
- Use `archivedAt` if archive behavior is implemented.
