import pytest

from ttrpg_dice import d


@pytest.fixture
def dietype(request: str) -> d:
    """
    Instatiate dice from string using `d` for `Dice`, at execution time.

    Intended for use in parameterised tests requiring Dice allowing for any instantiation errors to occur during
    execution and not test collection.

    Usage:
    ```
    @pytest.mark.parametrize(
        ["dietype", "description"],
        [
            ("d(4)", "d4"),
        ],
        indirect=["dietype"],
    )
    """
    return eval(request.param)  # noqa: S307
