# tuiify

[![CI](../../actions/workflows/ci.yml/badge.svg)](../../actions/workflows/ci.yml)
[![Publish](../../actions/workflows/publish.yml/badge.svg)](../../actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/tuiify)](https://pypi.org/project/tuiify/)
[![Python versions](https://img.shields.io/pypi/pyversions/tuiify)](https://pypi.org/project/tuiify/)
[![Downloads](https://img.shields.io/pypi/dm/tuiify)](https://pypi.org/project/tuiify/)
[![License](https://img.shields.io/pypi/l/tuiify)](https://pypi.org/project/tuiify/)

Turn typed Python functions into full-screen terminal forms.

`tuiify` generates a [Textual](https://textual.textualize.io/) interface from a function's signature and docstring. Add one decorator, call the function with no arguments, and get a form with sensible widgets, defaults, validation, and result handling.

## Features

- Generate forms from standard Python type annotations
- Map `str`, `int`, `float`, `bool`, and `Literal` to native Textual widgets
- Pre-populate fields from default parameter values
- Display return values in the running application
- Render validation errors and function tracebacks without crashing the terminal
- Bypass the UI by passing arguments directly

## Installation

```bash
pip install tuiify
```

For development, install the package with its test dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Quick start

```python
from typing import Literal

from tuiify import interactive


@interactive
def greet(
    name: str,
    count: int = 1,
    style: Literal["formal", "casual"] = "casual",
) -> str:
    """Create a greeting."""
    return f"{style} greeting for {name} ({count})"


result = greet()
```

Save the example as `example.py` and run it from a terminal:

```bash
python example.py
```

Calling `greet()` with no arguments opens a full-screen form. The generated fields are:

| Annotation | Widget |
| --- | --- |
| `str` | Text input |
| `int`, `float` | Numeric input with conversion and validation |
| `bool` | Checkbox |
| `Literal[...]` | Select dropdown |

Submit with the on-screen button or `Ctrl+S`. The result is shown in the lower pane. Invalid values and exceptions are displayed in the same app as formatted errors.

## Direct calls

Calls with arguments behave like the original function and do not open the UI:

```python
greet(name="Ada", count=2, style="formal")
```

## How it works

1. `@interactive` inspects the decorated function's signature.
2. `tuiify` creates a Textual widget for each supported parameter.
3. Defaults are loaded into the form automatically.
4. Submitting the form converts values back to the annotated types.
5. The function result or a formatted traceback appears in the result pane.

## Development

Install the local checkout in editable mode:

```bash
python -m pip install -e .
```

Run the checks locally:

```bash
python -m pytest
python -m compileall -q src
python -m build
```

The package supports Python 3.9 and newer. CI runs tests and builds on pull requests and pushes to `main`.

## Publishing

Publishing is triggered by pushing a version tag beginning with `v`:

```bash
git tag v0.1.0
git push origin v0.1.0
```

The publish workflow builds the wheel and source distribution, creates a GitHub release with generated notes, attaches the distributions to that release, and publishes them to PyPI. Configure a repository or `pypi` environment secret named `PYPI_TOKEN` before pushing a tag.

The workflow uses the tag for the release name. Keep the tag version aligned with the version in `pyproject.toml`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow and [SECURITY.md](SECURITY.md) for private vulnerability reports.
