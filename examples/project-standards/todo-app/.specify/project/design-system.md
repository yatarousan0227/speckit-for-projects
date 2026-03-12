# Design System

This document defines the local UI system rules for the ToDo application. The project does not assume an external component library, so these rules are the reference for screen design, implementation, and Storybook coverage.

## Component Taxonomy

- Foundations:
  - semantic color tokens for `surface`, `text`, `border`, `accent`, `success`, `warning`, and `danger`
  - spacing tokens based on a 4px scale
  - typography styles for page title, section title, body text, helper text, and metadata
- Primitives:
  - `Button`, `TextField`, `TextArea`, `Checkbox`, `Select`, `Badge`, `Dialog`, `Toast`, `Card`, `EmptyState`
- Feature components:
  - `TaskComposer`, `TaskFilterBar`, `TaskList`, `TaskRow`, `TaskSummary`, `TaskEmptyState`
- Screens:
  - screens compose feature components and layout primitives only
  - screens must not introduce one-off styling that should instead become a primitive or feature component

## Atomic Design Structure

- The component hierarchy follows Atomic Design: `atoms -> molecules -> organisms -> templates -> pages`.
- `atoms` contain styling-safe primitives such as `Button`, `Checkbox`, and `Badge`.
- `molecules` combine a small number of atoms into reusable units such as `FieldWithHint` or `TaskStatusBadge`.
- `organisms` define feature sections such as `TaskComposer`, `TaskFilterBar`, and `TaskList`.
- `templates` define layout skeletons for screens without hard-coding page-specific copy.
- `pages` assemble templates and feature data for concrete review states in Storybook.

Example directory shape:

```text
src/components/
  atoms/
    Button/
    Checkbox/
    Badge/
  molecules/
    FieldWithHint/
    TaskStatusBadge/
  organisms/
    TaskComposer/
    TaskFilterBar/
    TaskList/
  templates/
    TaskInboxTemplate/
  pages/
    TaskInboxPage/
```

## Composition Rules

- Task state is communicated with a combination of copy, iconography, and color. Color alone must never indicate completion, overdue state, or validation result.
- Forms use the same field layout pattern: label, control, helper text, then error text.
- Task rows keep action density low: complete toggle, main content, due date, and overflow actions stay visually grouped and keyboard reachable.
- Empty, loading, and error states must use dedicated reusable components rather than inline ad hoc markup.

## Variant Rules

- `Button` supports `primary`, `secondary`, `ghost`, and `danger`.
- `Badge` supports `neutral`, `success`, and `warning`.
- Inputs support `default`, `error`, `disabled`, and `readOnly`.
- Interactive destructive actions must require either a `danger` variant or a confirmation dialog.

## Accessibility Rules

- All interactive controls must expose an accessible name.
- Keyboard focus must remain visible on every interactive primitive.
- Checkbox, filter, and dialog flows must be fully operable without a pointer device.
- Minimum touch target size is 44x44 CSS pixels for controls used on mobile layouts.

## Storybook Expectations

- Every primitive and reusable feature component has at least one story.
- Stories for task-facing components include default, empty, validation-error, and overdue-task states where applicable.
- Visual review covers desktop and narrow mobile widths before merge.
- Story files follow the same Atomic Design layering so reviewers can navigate from primitive to screen state.

Example Storybook shape:

```text
ui-storybook/
  stories/
    atoms/
      Button.stories.js
    molecules/
      FieldWithHint.stories.js
    organisms/
      TaskList.stories.js
    templates/
      TaskInboxTemplate.stories.js
    pages/
      TaskInboxPage.stories.js
```

Example story titles:

- `Atoms/Button`
- `Molecules/FieldWithHint`
- `Organisms/TaskList`
- `Templates/TaskInboxTemplate`
- `Pages/TaskInboxPage`
