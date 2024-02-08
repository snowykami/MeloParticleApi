import math
from typing import Callable

import sympy


def conv2math_expr(func: Callable, var: str = 't') -> str:
    """Convert a Python function to a mathematical expression.

    Args:
        func: Python function
        var: Variable name

    Returns:
        str: Mathematical expression
    """
    t = sympy.symbols(var)
    return func(t)
