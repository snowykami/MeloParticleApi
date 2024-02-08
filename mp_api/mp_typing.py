from typing import Tuple, List, Dict

T_Num = float | int
T_Pos = Tuple[float | int | str, float | int | str, float | int | str]
T_Vec3 = Tuple[float | int, float | int, float | int]

T_ARGB = Tuple[int, int, int, int]
T_RGB = Tuple[int, int, int]
T_Color = T_RGB | T_ARGB | str | int
