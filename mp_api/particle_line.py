import math
from typing import Callable, Tuple

from mp_api import Arc2, T_Num, line2by2p


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
        self.length = length

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


def arc22pl(arc: Arc2, y_fun: Callable) -> ParticleLine:
    """
    Get the line of the arc
    :param y_fun:
    :param arc:
    :return:
    """
    # start_time与起始点的x相同,end_time与终点的x相同
    if arc.center is None:
        return ParticleLine(
            start_time=arc.start.x,
            end_time=arc.end.x,
            x_fun=lambda p: arc.start.x + (arc.end.x - arc.start.x) * p,
            # 抛物线
            y_fun=lambda t: y_fun(t),
            z_fun=lambda p: arc.start.y + (arc.end.y - arc.start.y) * p,
            length=arc.start.get_distance(arc.end)
        )
    return ParticleLine(
        start_time=arc.start.x,
        end_time=arc.end.x,
        x_fun=lambda p: arc.center.x + arc.radius * math.cos(math.atan2(arc.start.y - arc.center.y, arc.start.x - arc.center.x) + arc.get_delta_angle() * p),
        y_fun=y_fun,
        z_fun=lambda p: arc.center.y + arc.radius * math.sin(math.atan2(arc.start.y - arc.center.y, arc.start.x - arc.center.x) + arc.get_delta_angle() * p),
        length=arc.length
    )
