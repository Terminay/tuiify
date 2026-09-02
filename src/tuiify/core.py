"""Public decorator for turning typed functions into Textual forms."""

from functools import wraps
import inspect
from typing import Any, Callable, TypeVar, cast

from .app import DynamicFormApp

Function = TypeVar("Function", bound=Callable[..., Any])


def interactive(function: Function) -> Function:
    """Decorate a function with a zero-argument Textual form invocation."""
    signature = inspect.signature(function)

    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if args or kwargs:
            return function(*args, **kwargs)

        app = DynamicFormApp(function, signature)
        app.run()
        return app.result

    return cast(Function, wrapper)
