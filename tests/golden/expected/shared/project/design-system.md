# Design System

Use this file when the project has local UI system rules that are not fully explained by `.specify/project/tech-stack.md`.

If the project adopts an external design system such as Material Design, `shadcn/ui`, or another vendor library, document that choice in `tech-stack.md` first. When the adopted system already defines the project's component model and review workflow, this file can stay minimal or explicitly say that no additional local design system rules are needed.

## Applicability Check

- Adopted external design system, if any:
- Additional local rules beyond the adopted system:
- Decision:
  - `Fill this file` when the project defines its own component taxonomy, Storybook review workflow, naming rules, or accessibility rules
  - `Not applicable` when `tech-stack.md` already captures the adopted design system and there are no project-specific extensions

## Design System Decision

- State whether the project uses a local design system, an adopted external system, or a hybrid model.
- If the answer is `Not applicable`, write one short note here and stop.

Example minimal note:

```text
This project adopts Material Design through MUI. No additional local design system rules are defined beyond what is recorded in `.specify/project/tech-stack.md`.
```

## Component Taxonomy

- State whether the project uses Atomic Design.
- If yes, define how each layer is used in this repository:
  - `atoms`
  - `molecules`
  - `organisms`
  - `templates`
  - `pages`
- If no, replace the list above with the actual component hierarchy used by the project.
- Record the expected source directories for shared UI components.

## Storybook Review Model

- State whether Storybook is required for UI review.
- Keep shared screen catalogs and shared navigation rules in `designs/common_design/ui/`. This file and project-level Storybook cover component taxonomy and review workflow, not the canonical screen-transition contract.
- Record where project-level Storybook files live, for example:
  - `.specify/project/ui-storybook/stories/`
  - `.specify/project/ui-storybook/components/`
  - `.specify/project/ui-storybook/.storybook/`
- State whether feature-level bundles under `designs/specific_design/<design-id>/ui-storybook/` extend the project-level design system or replace it.
- Define story title conventions, story naming rules, and required review states.
- Define which UI layers must have stories, such as all shared components, only feature components, or full screen states.

## Rules To Define

- Naming and variants:
  - component names
  - prop or variant names
  - status and state naming
- Composition:
  - when to create a new atom, molecule, or organism
  - when screen-specific UI may stay local
- Tokens and layout primitives:
  - spacing, typography, color, elevation, breakpoints
- Accessibility:
  - keyboard interaction
  - focus visibility
  - semantic labels
- Review policy:
  - required Storybook states
  - visual review expectations
  - handoff rules to implementation
