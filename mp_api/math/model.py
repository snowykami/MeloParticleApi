import math
from enum import Enum
from typing import List

import numpy as np

from .geometry import Point3
from .utils import arithmetic_sequence
from ..typing import T_Num


class ModeEnum(Enum):
    """表示模型点组的生成模式枚举值类。

    - VERTEX: 仅顶点模式，不支持球体类。
    - LINE: 仅边模式，不支持球体类。
    - SURFACE: 仅表面模式。
    - SOLID: 实心模式。
    """
    VERTEX = 0
    LINE = 1
    SURFACE = 2
    SOLID = 3


class PointModel:
    """表示模型点组的生成类。
    """

    @staticmethod
    def cube(length: T_Num, density: T_Num, anchor: Point3 = Point3(0.5, 0.5, 0.5), mode: str = ModeEnum.SURFACE) -> list[Point3]:
        """
        返回立方体模型的点组。
        Args:
            length: 边长
            density: 密度: 单位长度内的点数
            anchor: 锚点, 默认为(0.5, 0.5, 0.5), 取值在0-1之间
            mode: 取点模式: 支持DOT、LINE、SURFACE和SOLID

        Returns:
            list[Point3]: 点组
        """
        num_per_side = int(density * length)
        points = []
        points_per_side = arithmetic_sequence(0, length, num_per_side)
        dx = -length * anchor.x
        dy = -length * anchor.y
        dz = -length * anchor.z

        if mode == ModeEnum.VERTEX:
            for x in [0, length]:
                for y in [0, length]:
                    for z in [0, length]:
                        points.append(Point3(x, y, z))

        elif mode == ModeEnum.LINE:
            for i in points_per_side:
                for j in [0, length]:
                    for k in [0, length]:
                        points.append(Point3(i + dx, j + dy, k + dz))
                        points.append(Point3(k + dx, i + dy, j + dz))
                        points.append(Point3(j + dx, k + dy, i + dz))

        elif mode == ModeEnum.SURFACE:
            for i in points_per_side:
                for j in points_per_side:
                    for k in [0, length]:
                        points.append(Point3(i + dx, j + dy, k + dz))
                        points.append(Point3(k + dx, i + dy, j + dz))
                        points.append(Point3(j + dx, k + dy, i + dz))

        elif mode == ModeEnum.SOLID:
            for x in points_per_side:
                for y in points_per_side:
                    for z in points_per_side:
                        points.append(Point3(x, y, z))

        else:
            raise ValueError(f"不支持的模式: {mode}")

        return points

    @staticmethod
    def sphere_ave(radius: T_Num, density: T_Num, mode: str = ModeEnum.SURFACE) -> list[Point3]:
        """
        返回球体模型的点组(均匀取点)
        公式支持@不背完牛津高阶不改名
        Args:
            radius: 半径
            density: 密度: 单位面积内的点数
            mode: 取点模式: 仅支持SURFACE和SOLID

        Returns:
            list[Point3]: 点组
        """
        points: List[Point3] = []

        surface_area = 4 * math.pi * radius ** 2
        num = surface_area * density
        for i in range(num):
            r_temp = radius
            phi = math.acos(-1 + ((2.0 * i - 1.0) / num))  # φ
            theta = math.sqrt(num * math.pi) * phi  # θ
            x = r_temp * math.cos(theta) * math.sin(phi)
            y = r_temp * math.sin(theta) * math.sin(phi)
            z = r_temp * math.cos(phi)
            points.append(Point3(x, y, z))
        if mode == ModeEnum.SURFACE:
            return points
        elif mode == ModeEnum.SOLID:
            return points
        else:
            raise ValueError(f"不支持的模式: {mode}")

    @staticmethod
    def sphere_cube(radius: T_Num, density: T_Num, mode: str = ModeEnum.SURFACE) -> list[Point3]:
        """
        返回球体模型的点组(遍历立方体取点)
        Args:
            radius: 半径
            density: 密度: 单位长度内的点数(与cube有关)
            mode: 取点模式: 仅支持SURFACE和SOLID

        Returns:
            list[Point3]: 点组
        """
        pass
