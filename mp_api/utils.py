import math
import random
from typing import Callable, Tuple

import sympy

from mp_api import Color


def func2math_exp(func: Callable | str,
                  var: str = 't'
                  ) -> str:
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


def delta(*args) -> Tuple[str,]:
    """Convert a list of minecraft pos to a list of delta pos.
    """
    place = 6
    str_list = []
    for x in args:
        str_list.append(f'~{x:.5f}')

    return tuple(str_list)

class Enum:
    @staticmethod
    def get_color_block(index: int) -> str:
        """Enum color block
        :param index:
        :return:
        """
        color_blocks = [
                "black_concrete",
                "black_glazed_terracotta",
                "black_terracotta",
                "blue_concrete",
                "blue_glazed_terracotta",
                "blue_terracotta",
                "brown_concrete",
                "brown_glazed_terracotta",
                "brown_terracotta",
                "cyan_concrete",
                "cyan_glazed_terracotta",
                "cyan_terracotta",
                "gray_concrete",
                "gray_glazed_terracotta",
                "gray_terracotta",
                "green_concrete",
                "green_glazed_terracotta",
                "green_terracotta",
                "light_blue_concrete",
                "light_blue_glazed_terracotta",
                "light_blue_terracotta",
                "light_gray_concrete",
                "light_gray_glazed_terracotta",
                "light_gray_terracotta",
                "lime_concrete",
                "lime_glazed_terracotta",
                "lime_terracotta",
                "magenta_concrete",
                "magenta_glazed_terracotta",
                "magenta_terracotta",
                "orange_concrete",
                "orange_glazed_terracotta",
                "orange_terracotta",
                "pink_concrete",
                "pink_glazed_terracotta",
                "pink_terracotta",
                "purple_concrete",
                "purple_glazed_terracotta",
                "purple_terracotta",
                "red_concrete",
                "red_glazed_terracotta",
                "red_terracotta",
                "terracotta",
                "white_concrete",
                "white_glazed_terracotta",
                "white_terracotta",
                "yellow_concrete",
                "yellow_glazed_terracotta",
                "yellow_terracotta",
        ]
        return color_blocks[index]

    @staticmethod
    def get_color_falling_block(index: int) -> str:
        """Enum color falling block
        :param index:
        :return:
        """
        color_blocks = [
                "black_concrete_powder",
                "blue_concrete_powder",
                "brown_concrete_powder",
                "cyan_concrete_powder",
                "gray_concrete_powder",
                "green_concrete_powder",
                "light_blue_concrete_powder",
                "light_gray_concrete_powder",
                "lime_concrete_powder",
                "magenta_concrete_powder",
                "orange_concrete_powder",
                "pink_concrete_powder",
                "purple_concrete_powder",
                "red_concrete_powder",
                "white_concrete_powder",
                "yellow_concrete_powder",
        ]
        return color_blocks[index]

    @staticmethod
    def get_color(index: int) -> Color:
        """Enum color
        :param index:
        :return: #FFFFFF
        """
        colors = [
                Color("#FFFF6E"),
                Color("#FF6E6E"),
                Color("#FF6EFF"),
                Color("#6E6EFF"),
                Color("#6EFF6E"),
                Color("#6EFFFF"),
                Color("#6E6E6E"),
                Color("#FFFFFF"),
                Color("#FF6E00"),
                Color("#FFD800"),
                Color("#FF00FF"),
                Color("#00FFFF"),
                Color("#00FF00"),
                Color("#0000FF"),
                Color("#FF0000"),
                Color("#000000"),
        ]
        return colors[index]
