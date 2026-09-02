from tuiify import interactive


def test_direct_call_bypasses_ui() -> None:
    calls = []

    @interactive
    def add(left: int, right: int) -> int:
        calls.append((left, right))
        return left + right

    assert add(2, right=3) == 5
    assert calls == [(2, 3)]
