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
                "blue_concrete",
                "brown_concrete",
                "cyan_concrete",
                "gray_concrete",
                "green_concrete",
                "light_blue_concrete",
                "light_gray_concrete",
                "lime_concrete",
                "magenta_concrete",
                "orange_concrete",
                "pink_concrete",
                "purple_concrete",
                "red_concrete",
                "white_concrete",
                "yellow_concrete",

        ]
        return color_blocks[index % len(color_blocks)]

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
        return color_blocks[index % len(color_blocks)]

    @staticmethod
    def get_color(index: int) -> Color:
        """Enum color by concrete
        :param index:
        :return: #FFFFFF
        """
        colors = [
                Color('#FFA500'),
                Color('#FFFF00'),
                Color('#00FFFF'),
                Color('#FF0000'),
                Color('#D3D3D3'),
                Color('#FF00FF'),

                Color('#000000'),
                Color('#0000FF'),
                Color('#A52A2A'),
                Color('#808080'),
                Color('#008000'),
                Color('#ADD8E6'),
                Color('#00FF00'),

                Color('#FFC0CB'),
                Color('#800080'),
                Color('#FFFFFF'),

        ]
        return colors[index % len(colors)]
