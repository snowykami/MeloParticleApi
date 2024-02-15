import math
from typing import Callable, Tuple

from mp_api import Arc2, T_Num


class ParticleLine:
    def __init__(self,
                 start_time: T_Num,
                 end_time: T_Num,
                 x_fun: Callable[[T_Num], T_Num],
                 y_fun: Callable[[T_Num], T_Num],
                 z_fun: Callable[[T_Num], T_Num],
                 ):
        """
        :param start_time: 起始时间
        :param end_time: 结束时间
        :param x_fun: 以age/life为参数
        :param y_fun:
        :param z_fun:
        """
        self.start_time = start_time
        self.end_time = end_time
        self.x_fun = x_fun
        self.y_fun = y_fun
        self.z_fun = z_fun

    def get_pos(self,
                p: T_Num
                ):
        """
        :param p: 0-1
        :return:
        """
        return self.x_fun(p), self.y_fun(p), self.z_fun(p)

    def get_vector3(self,
                    p: T_Num,
                    delta: T_Num = 0.001
                    ):
        """
        :param delta:
        :param p: 0-1
        :return:
        """
        # 求取该点的切向量
        x1, y1, z1 = self.get_pos(p - delta)
        x2, y2, z2 = self.get_pos(p + delta)
        return (x2 - x1) / (2 * delta), (y2 - y1) / (2 * delta), (z2 - z1) / (2 * delta)


def arc22pl(arc: Arc2) -> ParticleLine:
    """
    Get the line of the arc
    :param arc:
    :return:
    """
    # start_time与起始点的x相同,end_time与终点的x相同
    return ParticleLine(
        start_time=arc.center.x + arc.radius * math.cos(arc.start),
        end_time=arc.center.x + arc.radius * math.cos(arc.end),
        x_fun=lambda t: arc.center.x + arc.radius * math.cos(t),
        y_fun=lambda t: 0,
        z_fun=lambda t: arc.center.y + arc.radius * math.sin(t),
    )