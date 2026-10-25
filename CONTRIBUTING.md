# Contributing

Thanks for taking a look. This is a small single-file tool, and the process is
deliberately lightweight.

## Before you start

- For a bug, open an issue with your distro, desktop environment, the exact
  command you ran, and the output (`appim list` is often useful).
- For a behaviour change or a new subcommand, open an issue first so we can agree
  on the design before you write code.

## Development setup

```sh
git clone https://github.com/new-monkey/appim.git
cd appim

make test    # stdlib unittest, no dependencies
make lint    # ruff check + format check
make check   # both
```

Optional: install the working copy and try it against a real AppImage.

```sh
make install
appim install ~/Downloads/Some-App-x86_64.AppImage
appim list
appim remove "Some App"
```

The unit tests never touch your real `$HOME`: they only exercise pure functions
(`slug`, `_sanitize`, `parse_desktop`, `rewrite_desktop`, `quote_exec_arg`) and
run the CLI with arguments that fail before any filesystem write.

## Code conventions

- Python 3.8+ compatible; **standard library only**. Please don't add runtime
  dependencies to a script whose selling point is that it has none.
- Formatting and linting are enforced by `ruff` (config in `pyproject.toml`).
  Run `make check` before pushing.
- Keep the tool a single file. If something genuinely needs its own module, that
  is a discussion for an issue, not a drive-by refactor.
- New behaviour needs a test in `tests/test_appim.py`.

## Commit messages

Conventional Commits style, imperative mood:

```
feat: add --prefix flag
fix: keep Exec arguments containing spaces
docs: document the hicolor fallback order
test: cover localized desktop keys
```

## Pull requests

1. Fork, branch from `main`, keep the change focused.
2. Add or update tests; make sure `make check` passes.
3. Describe **what** changed and **why**, plus how you verified it.
4. Update `CHANGELOG.md` under `## [Unreleased]` for user-visible changes.

CI runs the test matrix (Python 3.9–3.13 on Ubuntu) plus ruff on every push and
pull request.

## License

By contributing you agree that your contributions are licensed under the
[MIT License](LICENSE).
