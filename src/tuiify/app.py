"""Textual application used by the interactive decorator."""

import inspect
import traceback
from typing import Any, Callable, List

from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Button, Checkbox, Header, Label, RichLog

from .mapper import FieldSpec, create_field, read_value


class DynamicFormApp(App):
    """Render a function signature as a full-screen form."""

    BINDINGS = [("ctrl+s", "submit", "Submit")]
    CSS = """
    Screen {
        layout: vertical;
    }

    #form-pane {
        height: 1fr;
        border: round $primary;
        padding: 1 2;
    }

    #form {
        height: 1fr;
    }

    .field-label {
        margin-top: 1;
    }

    Input, Select, Checkbox {
        margin-bottom: 1;
    }

    #submit {
        width: 100%;
        margin-top: 1;
    }

    #result-pane {
        height: 1fr;
        border: round $success;
        padding: 1 2;
    }

    #result-pane.error {
        border: round $error;
        color: $error;
    }
    """

    def __init__(self, function: Callable[..., Any], signature: inspect.Signature) -> None:
        super().__init__()
        self.function = function
        self.signature = signature
        self.result: Any = None
        self.fields: List[FieldSpec] = []

    def compose(self) -> ComposeResult:
        self.fields = [
            create_field(parameter)
            for parameter in self.signature.parameters.values()
            if parameter.kind not in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            )
        ]
        yield Header(show_clock=True)
        with Vertical(id="form-pane"):
            yield Label(self.function.__doc__ or "Fill in the parameters and submit.")
            with VerticalScroll(id="form"):
                for field in self.fields:
                    if not isinstance(field.widget, Checkbox):
                        yield Label(field.label, classes="field-label")
                    yield field.widget
                yield Button("Submit", id="submit", variant="primary")
        with Vertical(id="result-pane"):
            yield Label("Result")
            yield RichLog(id="result", highlight=True, markup=False)

    def action_submit(self) -> None:
        """Validate the form and show the function result or traceback."""
        try:
            values = {field.name: read_value(field) for field in self.fields}
            result = self.function(**values)
        except Exception:
            self._show_error(traceback.format_exc())
            return

        result_view = self.query_one("#result", RichLog)
        result_view.clear()
        result_view.write(repr(result))
        self.result = result
        self.query_one("#result-pane").remove_class("error")

    def _show_error(self, message: str) -> None:
        result_view = self.query_one("#result", RichLog)
        result_view.clear()
        result_view.write(message)
        self.query_one("#result-pane").add_class("error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            self.action_submit()
