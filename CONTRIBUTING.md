# Contributing

## Scope

Contributions are welcome for CLI behavior, scaffold templates, documentation, examples, and validation rules.

For larger changes, open an issue first so the intended workflow and artifact shape can be agreed before implementation starts.

## Development Setup

Requirements:

- Python 3.12+
- `uv`
- Node.js and npm if you need to verify Storybook example bundles

Setup:

```bash
uv sync --dev
uv run sdd --help
```

## Recommended Checks

Run these before opening a pull request:

```bash
uv run pytest
uv run ruff check .
uv run mypy src
```

If you changed Storybook-related templates or example bundles, also verify at least the affected bundle with:

```bash
npm install
npm run build-storybook
```

## Change Guidelines

- Keep the CLI surface small unless there is a clear need for a new command.
- Prefer improving prompts, templates, and validation rules over adding framework-like behavior.
- Preserve the `project` / `common_design` / `specific_design` separation.
- Do not introduce feature-local copies of shared design truth.
- Update README, guides, or examples when behavior or expected artifacts change.
- Add or update tests when changing scaffold output, validation logic, or command behavior.

## Pull Requests

Please keep pull requests focused and include:

- the problem being solved
- the reason for the chosen approach
- any repository paths or generated artifacts affected
- test or verification results

If the change affects generated output, include the expected before/after behavior in the PR description.

## Documentation Changes

Documentation fixes do not need a full design discussion, but they should still be precise and consistent with the current CLI behavior.

## License

By contributing to this repository, you agree that your contributions will be licensed under the [MIT License](LICENSE).

