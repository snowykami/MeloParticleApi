import math
from typing import Callable, List, Tuple

import numpy as np

from . import func2math_exp
from .mp_typing import T_Pos
from .particle_line import ParticleLine, arc22pl
from .mp_math import Arc2, Point2, Point3, Segment2, T_Num


def points_2_group(points: List[Point3]) -> List[List[Point3]]:
    """
    把x相同的点分为一组列表储存，且列表内按z排序，整数坐标自动加上0.5
    :param points:
    :return:
    """
    point_groups = []
    points.sort(key=lambda x: x.x)
    # 先分组
    for point in points:
        if len(point_groups) == 0:
            point_groups.append([point])
        else:
            if point_groups[-1][0].x == point.x:
                point_groups[-1].append(point)
            else:
                point_groups.append([point])
    # 按照x排序列表
    point_groups.sort(key=lambda x: x[0].x)
    # 按照z排序列表中的点
    for group in point_groups:
        group.sort(key=lambda x: x.z)
    return point_groups


def connect_points(start_num: int,
                   end_num: int
                   ) -> List[Tuple[int, int]]:
    connections = []
    if start_num >= end_num:
        # Each end point connects to one start point
        for i in range(end_num):
            connections.append((i, i))
    else:
        # Some start points connect to multiple end points
        each_num = end_num // start_num
        remainder = end_num % start_num
        for i in range(start_num):
            for j in range(each_num + (i < remainder)):
                connections.append((i, i * each_num + j + min(i, remainder)))
    return connections


# 进行一个🐟的摸，稍等
class Soma:
    @staticmethod
    def soma3_2d(point_groups: List[List[Point3]]) -> List[ParticleLine]:
        """
        计算平面soma3，返回带有ParticleLine的列表，建议自行添加起始点以便美观
        Soma3曲线在两个点之间用圆弧连接，且两个点处的切线方向相同
        :param point_groups: 处理后的点组
        :return:
        """
        lines = []
        # 起始线
        last_arc_list = []
        # 制造假圆弧
        for p in point_groups[0]:
            cp = Point2(p.x, p.z - 1)
            sp = Point2(p.x - 1, p.z - 1)
            ep = p.point2mc
            last_arc_list.append(Arc2(cp, sp, ep, -1))
        for i, start_group, end_group in zip(range(len(point_groups[:-1])), point_groups[:-1], point_groups[1:]):
            start_num = len(start_group)
            end_num = len(end_group)
            connections = connect_points(start_num, end_num)

            this_arc_list: List[Arc2] = []  # 本次的Arc临时列表
            for conn in connections:
                # 两点连接域
                startp2: Point2 = start_group[conn[0]].point2mc
                endp2: Point2 = end_group[conn[1]].point2mc
                path_seg = Segment2(startp2, endp2)  # 位移线段
                last_arc = last_arc_list[conn[0]]
                if last_arc.center is None:
                    # 上一个弧是假弧的特殊情况

                    last_path_seg = Segment2(last_arc.start, last_arc.end)
                    zero_line = last_path_seg.line.get_perpendicular_line(last_arc.end)
                    center = zero_line.get_intersection(path_seg.perpendicular_bisector)  # 圆心
                    croter_line = Segment2(startp2, center).line
                    v1 = center.get_vector2(startp2)
                else:
                    croter_line = Segment2(last_arc.center, last_arc.get_pos(1.0)).line  # 末向量/穿心线段/判定线段(建议用向量夹角判断，不要用点在线上，会出现精度错误)
                    v1 = startp2.get_vector2(last_arc.center)

                if croter_line.is_parallel(path_seg.perpendicular_bisector):
                    center = None
                else:
                    center = croter_line.get_intersection(path_seg.perpendicular_bisector)

                v2 = startp2.get_vector2(endp2)

                if v1.get_angle(v2) > math.pi / 2:
                    dire = -1 * last_arc.direction
                elif v1.get_angle(v2) == math.pi / 2:
                    dire = last_arc.direction
                else:
                    dire = last_arc.direction

                arc2 = Arc2(center, startp2, endp2, dire)  # 生成Arc2
                this_arc_list.append(arc2)  # 加入本次的Arc临时列表

                particle_line = arc22pl(arc2, lambda t: start_group[conn[0]].y + (end_group[conn[1]].y - start_group[conn[0]].y) * t)
                lines.append(particle_line)
            last_arc_list = this_arc_list
        return lines

    @staticmethod
    def line_3d(point_groups: List[List[Point3]]) -> List[ParticleLine]:
        """
        计算3d线，返回带有ParticleLine的列表，建议自行添加起始点以便美观
        :param point_groups: 处理后的点组
        :return:
        """
        lines = []
        for i, start_group, end_group in zip(range(len(point_groups[:-1])), point_groups[:-1], point_groups[1:]):
            start_num = len(start_group)
            end_num = len(end_group)
            connections = connect_points(start_num, end_num)
            for conn in connections:
                startp3: Point3 = start_group[conn[0]]
                endp3: Point3 = end_group[conn[1]]
                particle_line = ParticleLine(
                    start_time=startp3.x,
                    end_time=endp3.x,
                    x_fun=lambda p, sx=startp3.x, ex=endp3.x: sx + (ex - sx) * p,
                    y_fun=lambda p, sy=startp3.y, ey=endp3.y: sy + (ey - sy) * p,
                    z_fun=lambda p, sz=startp3.z, ez=endp3.z: sz + (ez - sz) * p,
                    length=startp3.get_distance(endp3)
                )
                lines.append(particle_line)
        return lines


class Struct:
    # 这个类预定了一些形状样式的相对坐标列表
    @staticmethod
    def cube(length: T_Num = 1, density: T_Num = 0.1, padding: str = 'p', anchor: T_Pos = (0.5, 0.5, 0.5)) -> List[Point3]:
        """
        生成正方体
        :param anchor: 锚点，0.5为中心，0为左/下/前，1为右/上/后
        :param length: 边长
        :param density: 密度
        :param padding: 填充参数 p：仅8个顶点，l：仅12条边缘，s：仅6个表面，b：全部体
        :return:
        """
        num_per_side = int(length / density) + 1
        points = []
        # 以中心生成相对坐标点
        for i in range(num_per_side):
            for j in range(num_per_side):
                for k in range(num_per_side):
                    # p 仅8个顶点
                    if padding == 'p':
                        if (i == 0 or i == num_per_side - 1) and (j == 0 or j == num_per_side - 1) and (k == 0 or k == num_per_side - 1):
                            points.append(Point3(i * density - length * anchor[0], j * density - length * anchor[1], k * density - length * anchor[2]))
                    # l 仅12条边缘
                    elif padding == 'l':
                        if (i == 0 or i == num_per_side - 1) and (j == 0 or j == num_per_side - 1) and (k == 0 or k == num_per_side - 1):
                            points.append(Point3(i * density - length * anchor[0], j * density - length * anchor[1], k * density - length * anchor[2]))
                        elif (i == 0 or i == num_per_side - 1) and (j == 0 or j == num_per_side - 1):
                            points.append(Point3(i * density - length * anchor[0], j * density - length * anchor[1], k * density - length * anchor[2]))
                        elif (i == 0 or i == num_per_side - 1) and (k == 0 or k == num_per_side - 1):
                            points.append(Point3(i * density - length * anchor[0], j * density - length * anchor[1], k * density - length * anchor[2]))
                        elif (j == 0 or j == num_per_side - 1) and (k == 0 or k == num_per_side - 1):
                            points.append(Point3(i * density - length * anchor[0], j * density - length * anchor[1], k * density - length * anchor[2]))
                    # s 仅6个表面
                    elif padding == 's':
                        if i == 0 or i == num_per_side - 1 or j == 0 or j == num_per_side - 1 or k == 0 or k == num_per_side - 1:
                            points.append(Point3(i * density - length * anchor[0], j * density - length * anchor[1], k * density - length * anchor[2]))
                    elif padding == 'b':
                        points.append(Point3(i * density - length * anchor[0], j * density - length * anchor[1], k * density - length * anchor[2]))
                    else:
                        raise ValueError('padding参数错误')
        return points

    @staticmethod
    def sphere(radius: T_Num = 1, density: T_Num = 0.1, padding: str = 'p', anchor: T_Pos = (0, 0, 0)) -> List[Point3]:
        """
        生成球体
        :param anchor: 锚点，0.5为中心，0为左/下/前，1为右/上/后
        :param radius: 半径
        :param density: 密度
        :param padding: 填充参数 s：仅表面，b：全部体
        :return:
        """
        points = []
        # 以中心生成相对坐标点
        for i in np.arange(-radius, radius + density, density):
            for j in np.arange(-radius, radius + density, density):
                for k in np.arange(-radius, radius + density, density):
                    if padding == 's':
                        if abs(i ** 2 + j ** 2 + k ** 2 - radius ** 2) < density:
                            points.append(Point3(i - radius * anchor[0], j - radius * anchor[1], k - radius * anchor[2]))
                    elif padding == 'b':
                        if i ** 2 + j ** 2 + k ** 2 <= radius ** 2:
                            points.append(Point3(i - radius * anchor[0], j - radius * anchor[1], k - radius * anchor[2]))
                    else:
                        raise ValueError('padding参数错误')
        return points


class Animation:

    @staticmethod
    def diffusion(points: List[Point3], time: T_Num) -> List[Tuple[Callable, Callable, Callable]]:
        """
        扩散动画，从局部原点开始扩散指目标位置，用此公式给粒子的表达式配置后，粒子执行位置可以统一在原点
        :param points: 点列表
        :param time: 时间
        :return: 每个点的公式列表，单位是t
        """
        new_funcs = []
        for point in points:
            new_funcs.append(
                (
                        lambda t: (t / time) * point.x,
                        lambda t: (t / time) * point.y,
                        lambda t: (t / time) * point.z
                )
            )
        return new_funcs
