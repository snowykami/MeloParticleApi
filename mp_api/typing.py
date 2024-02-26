from typing import Callable, Tuple
"""
定义了一些常用的类型别名，用于类型提示。

类型别名:
    T_Num: 表示一个数字，可以是浮点数或整数。
    T_Pos: 表示一个位置，可以是三个浮点数、整数或字符串的元组。
    T_Vec3: 表示一个三维向量，是三个浮点数或整数的元组。
    T_Exp: 表示一个表达式，可以是字符串或可调用对象。
    T_ARGB: 表示一个ARGB颜色，是四个整数的元组。
    T_RGB: 表示一个RGB颜色，是三个整数的元组。
    T_Color: 表示一个颜色，可以是RGB或ARGB颜色、字符串或整数。
"""

from typing import Callable, Tuple

T_Num = float | int

T_Pos = Tuple[float | int | str, float | int | str, float | int | str]

T_Vec3 = Tuple[float | int, float | int, float | int]

T_Exp = str | Callable

T_ARGB = Tuple[int, int, int, int]
T_RGB = Tuple[int, int, int]
T_Color = T_RGB | T_ARGB | str | int
