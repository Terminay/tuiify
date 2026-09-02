"""Translate function parameters into form fields and typed values."""

from dataclasses import dataclass
import inspect
from typing import Any, Literal, get_args, get_origin

from textual.widget import Widget
from textual.widgets import Checkbox, Input, Select


@dataclass(frozen=True)
class FieldSpec:
    """Metadata needed to render and read one function parameter."""

    name: str
    label: str
    parameter: inspect.Parameter
    widget: Widget


def _display_label(name: str) -> str:
    return name.replace("_", " ").strip().title()


def create_field(parameter: inspect.Parameter) -> FieldSpec:
    """Create the appropriate Textual widget for a parameter."""
    annotation = parameter.annotation
    default = parameter.default
    input_value = "" if default is inspect.Parameter.empty else str(default)
    origin = get_origin(annotation)

    if origin is Literal:
        choices = get_args(annotation)
        options = [(str(choice), choice) for choice in choices]
        selected = None if default is inspect.Parameter.empty else default
        widget: Widget = Select(options, value=selected, id=f"field-{parameter.name}")
    elif annotation is bool:
        checked = False if default is inspect.Parameter.empty else bool(default)
        widget = Checkbox(_display_label(parameter.name), value=checked, id=f"field-{parameter.name}")
    else:
        widget = Input(
            value=input_value,
            placeholder=_placeholder(parameter),
            type="number" if annotation in (int, float) else "text",
            id=f"field-{parameter.name}",
        )

    return FieldSpec(
        name=parameter.name,
        label=_display_label(parameter.name),
        parameter=parameter,
        widget=widget,
    )


def _placeholder(parameter: inspect.Parameter) -> str:
    annotation = parameter.annotation
    if annotation in (int, float):
        return f"Enter a {annotation.__name__}"
    if parameter.default is inspect.Parameter.empty:
        return "Required"
    return "Optional"


def read_value(field: FieldSpec) -> Any:
    """Read and validate a widget value using the parameter annotation."""
    annotation = field.parameter.annotation
    widget = field.widget

    if isinstance(widget, Checkbox):
        return widget.value
    if isinstance(widget, Select):
        if widget.value is Select.BLANK:
            if field.parameter.default is not inspect.Parameter.empty:
                return field.parameter.default
            raise ValueError(f"{field.label} is required")
        return widget.value

    if not isinstance(widget, Input):
        raise TypeError(f"Unsupported widget for {field.name}")

    raw_value = widget.value.strip()
    if not raw_value:
        if field.parameter.default is not inspect.Parameter.empty:
            return field.parameter.default
        raise ValueError(f"{field.label} is required")

    if annotation is int:
        try:
            return int(raw_value)
        except ValueError as error:
            raise ValueError(f"{field.label} must be an integer") from error
    if annotation is float:
        try:
            return float(raw_value)
        except ValueError as error:
            raise ValueError(f"{field.label} must be a number") from error
    return raw_value
