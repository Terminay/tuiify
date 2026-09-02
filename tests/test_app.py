import inspect

from tuiify.app import DynamicFormApp


def make_signature() -> inspect.Signature:
    return inspect.Signature([
        inspect.Parameter("name", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=str),
    ])


async def test_submit_stores_function_result() -> None:
    app = DynamicFormApp(lambda name: f"Hello, {name}", make_signature())

    async with app.run_test():
        app.fields[0].widget.value = "Ada"
        app.action_submit()

        assert app.result == "Hello, Ada"
        assert not app.query_one("#result-pane").has_class("error")


async def test_submit_renders_function_traceback() -> None:
    def fail(name: str) -> None:
        raise RuntimeError(f"failed for {name}")

    app = DynamicFormApp(fail, make_signature())

    async with app.run_test():
        app.fields[0].widget.value = "Ada"
        app.action_submit()

        assert app.query_one("#result-pane").has_class("error")
        assert "RuntimeError" in "\n".join(str(line) for line in app.query_one("#result").lines)
