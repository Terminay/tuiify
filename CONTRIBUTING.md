# Contributing to tuiify

Thanks for taking the time to contribute.

## Development setup

`tuiify` supports Python 3.9 and newer.

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[dev]"
```

On macOS or Linux, activate the environment with `source .venv/bin/activate`.

## Before opening a pull request

```bash
python -m pytest
python -m compileall -q src
```

Keep changes focused, preserve the public `interactive` API, and add or update tests for behavior changes. Use clear commit messages and explain user-visible changes in the pull request description.

## Pull requests

1. Fork the repository and create a focused branch.
2. Make the smallest complete change that solves the issue.
3. Run the checks above.
4. Open a pull request using the repository template.

Bug fixes and documentation improvements are welcome. For larger changes, open an issue first so the design can be discussed before implementation.
