import inspect
from typing import Literal

import pytest
from textual.widgets import Checkbox, Input, Select

from tuiify.app import DynamicFormApp
from tuiify.mapper import read_value


def make_signature() -> inspect.Signature:
    return inspect.Signature(
        [
            inspect.Parameter("name", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=str),
            inspect.Parameter("count", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=int, default=2),
            inspect.Parameter("enabled", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=bool, default=True),
            inspect.Parameter(
                "mode",
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=Literal["fast", "safe"],
                default="safe",
            ),
        ]
    )


async def test_annotations_create_expected_widgets() -> None:
    app = DynamicFormApp(lambda name, count, enabled, mode: None, make_signature())

    async with app.run_test():
        assert isinstance(app.fields[0].widget, Input)
        assert isinstance(app.fields[1].widget, Input)
        assert isinstance(app.fields[2].widget, Checkbox)
        assert isinstance(app.fields[3].widget, Select)
        assert app.fields[1].widget.value == "2"
        assert app.fields[2].widget.value is True
        assert app.fields[3].widget.value == "safe"


async def test_values_are_converted_from_widgets() -> None:
    app = DynamicFormApp(lambda name, count, enabled, mode: None, make_signature())

    async with app.run_test():
        app.fields[0].widget.value = "Ada"
        app.fields[1].widget.value = "7"
        app.fields[2].widget.value = False
        app.fields[3].widget.value = "fast"

        assert [read_value(field) for field in app.fields] == ["Ada", 7, False, "fast"]


async def test_invalid_numeric_value_is_rejected() -> None:
    app = DynamicFormApp(lambda count: None, inspect.Signature([
        inspect.Parameter("count", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=int),
    ]))

    async with app.run_test():
        app.fields[0].widget.value = "not a number"
        with pytest.raises(ValueError, match="must be an integer"):
            read_value(app.fields[0])
