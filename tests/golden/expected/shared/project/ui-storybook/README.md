# Project UI Storybook

This directory holds the project-level UI foundation for local design systems.

Use it to review Atomic Design building blocks and major screen layouts before feature-specific design bundles are generated.

If `.specify/project/tech-stack.md` declares an adopted external design system such as Material Design or `shadcn/ui`, keep this directory minimal and document any exceptions in `.specify/project/design-system.md`.

## Purpose

- Define reusable `atoms`, `molecules`, `organisms`, `templates`, and `pages`
- Review major screen layouts before feature-level design starts
- Keep local HTML mocks and Storybook stories aligned with `.specify/project/design-system.md`

## Structure

- `components/atoms/`: design-system primitives
- `components/molecules/`: small composed UI units
- `components/organisms/`: feature sections
- `components/templates/`: major screen layouts without page-specific data binding
- `components/pages/`: representative project-level screens
- `stories/`: Storybook stories that mirror the same Atomic Design layers

## Local Review

```bash
npm install
npm run storybook
```

To verify the project-level UI scaffold:

```bash
npm run build-storybook
```

## Rules

- Use this directory for project-wide UI building blocks and representative layouts
- Put feature-specific review states in `designs/specific_design/<design-id>/ui-storybook/`
- Keep shared screen catalogs and shared navigation rules in `designs/common_design/ui/`
- Keep Storybook titles aligned with Atomic Design layers such as `Atoms/Button` and `Pages/TaskInboxPage`
