from typing import Any


def pytest_make_parametrize_id(val: Any, argname: str):
    """
    Format argument for `pytest.mark.parametrize` test item
    """
    return f'{argname}={val}'
