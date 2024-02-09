import math
from typing import Callable

import sympy


def func2math_exp(func: Callable | str, var: str = 't') -> str:
    """Convert a Python function to a mathematical expression.

    Args:
        func: Python function
        var: Variable name

    Returns:
        str: Mathematical expression
    """

    if isinstance(func, str):
        return func
    else:
        t = sympy.symbols(var)
        return func(t)
