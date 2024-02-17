import math
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from typing import Callable, List, Tuple
from .mp_math import Arc2, Point3
from .mp_typing import T_Num


class ParticleLine:
    def __init__(self,
                 start_time: T_Num,
                 end_time: T_Num,
                 x_fun: Callable[[T_Num], T_Num],
                 y_fun: Callable[[T_Num], T_Num],
                 z_fun: Callable[[T_Num], T_Num],
                 length: T_Num = 0
                 ):
        """
        代表三维空间中的粒子运动线。

        参数：
        - start_time (T_Num): 线的起始时间。
        - end_time (T_Num): 线的结束时间。
        - x_fun (Callable[[T_Num], T_Num]): 随进度系数变化定义 X 坐标的函数。
        - y_fun (Callable[[T_Num], T_Num]): 随进度系数变化定义 Y 坐标的函数。
        - z_fun (Callable[[T_Num], T_Num]): 随进度系数变化定义 Z 坐标的函数。
        - length (T_Num): 线的长度。
        """
        self.start_time = start_time
        self.end_time = end_time
        self.x_fun = x_fun
        self.y_fun = y_fun
        self.z_fun = z_fun
        self.length = length

    def __str__(self):
        return f"ParticleLine({self.start_time} -> {self.end_time} | from {self.get_pos(0)} to {self.get_pos(1)})"

    def get_pos(self,
                p: T_Num
                ) -> Tuple[T_Num, T_Num, T_Num]:
        """
        获取给定进度因子的位置。

        参数：
        - p (T_Num): 从 0 到 1 的进度因子。

        返回：
        Tuple[T_Num, T_Num, T_Num]: 在指定进度因子的位置的 X、Y、Z 坐标。
        """
        return self.x_fun(p), self.y_fun(p), self.z_fun(p)

    def get_vector3(self,
                    p: T_Num,
                    delta: T_Num = 0.001
                    ) -> Tuple[T_Num, T_Num, T_Num]:
        """
        获取给定进度因子的切线向量。

        参数：
        - p (T_Num): 从 0 到 1 的进度因子。
        - delta (T_Num): 用于数值微分的小增量。

        返回：
        Tuple[T_Num, T_Num, T_Num]: 在指定进度因子的切线向量。
        """
        # 使用数值微分计算给定点的切线向量
        x1, y1, z1 = self.get_pos(p - delta)
        x2, y2, z2 = self.get_pos(p + delta)
        return (x2 - x1) / (2 * delta), (y2 - y1) / (2 * delta), (z2 - z1) / (2 * delta)


def arc22pl(arc: Arc2, y_fun: Callable, npt: int = 20) -> ParticleLine:
    """
    将 Arc2 对象转换为用于粒子运动的 ParticleLine。

    参数：
    - arc (Arc2): 代表二维空间中弧的 Arc2 对象。
    - y_fun (Callable): 随时间变化定义 Y 坐标的函数。
    - npt (int): 每tick最大粒子数，超出后用直线代替(可改)。

    返回：
    ParticleLine: 代表转换后的弧的 ParticleLine 对象。
    """
    # 如果弧没有中心，创建一条直线
    if arc.center is None or arc.length / (arc.end.x - arc.start.x) > npt:
        return ParticleLine(
            start_time=arc.start.x,
            end_time=arc.end.x,
            x_fun=lambda p: arc.start.x + (arc.end.x - arc.start.x) * p,
            y_fun=lambda p: y_fun(p),
            z_fun=lambda p: arc.start.y + (arc.end.y - arc.start.y) * p,
            length=arc.start.get_distance(arc.end)
        )
    # 如果弧有中心，创建一个代表弧的 ParticleLine
    return ParticleLine(
        start_time=arc.start.x,
        end_time=arc.end.x,
        x_fun=lambda p: arc.center.x + arc.radius * math.cos(math.atan2(arc.start.y - arc.center.y, arc.start.x - arc.center.x) + arc.get_delta_angle() * p),
        y_fun=y_fun,
        z_fun=lambda p: arc.center.y + arc.radius * math.sin(math.atan2(arc.start.y - arc.center.y, arc.start.x - arc.center.x) + arc.get_delta_angle() * p),
        length=arc.length
    )


def arc2s2point3s(arc2s: List[Arc2], y_fun: Callable[[List[T_Num]], List[T_Num]], density: float = 0.1, max_npt: int = 40, threads: int = 1) -> List[Point3]:
    """
    将 Arc2 Soma3 对象列表转换为用于粒子运动的 Point3 对象列表。使用np和多线程批量计算，不经过粒子线阶段

    参数：
    - arc2s (List[Arc2]): 代表二维空间中弧的 Arc2 对象列表。
    - y_fun (Callable): 随时间变化定义 Y 坐标的函数。
    - density (float): 粒子线的密度。
    - max_npt (int): 每tick最大粒子数，超出后用直线代替(可改)。
    - threads (int): 线程数。

    返回：
    List[Point3]: 代表转换后的弧的 Point3 对象列表。
    """
    points = []

    # 把三角函数参数全部转成numpy数组
    x = [np.array([arc2.start.x, arc2.end.x]) for arc2 in arc2s]
    y = y_fun()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for arc2 in arc2s:
            points.append(executor.submit(arc22pl, arc2, y_fun))
