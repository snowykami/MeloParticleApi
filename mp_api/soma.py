import math
from typing import List, Tuple

from mp_api import Arc2, Line2, Point2, Point3, Segment2, Vector2, line2by2p
from mp_api.particle_line import ParticleLine, arc22pl


def points_2_group(points: List[Point3]) -> List[List[Point3]]:
    """
    把x相同的点分为一组列表储存，且列表内按z排序
    :param points:
    :return:
    """
    point_groups = []
    # 先分组
    for point in points:
        if len(point_groups) == 0:
            point_groups.append([point])
        else:
            if points[-1].x == point.x:
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
class Style:
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
            cp = Point2(p.x-1, p.z)
            sp = Point2(p.x-1, p.z-1)
            ep = Point2(p.x, p.z)
            last_arc_list.append(Arc2())
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

                croter_seg = Segment2(last_arc.center, last_arc.get_pos(1.0))  # 末向量/穿心线段/判定线段(建议用向量夹角判断，不要用点在线上，会出现精度错误)


                # 计算圆弧
                # if i == 0:
                #
                #     # 圆弧中心
                #     cp2 = path_seg.perpendicular_bisector.get_intersection(zero_line)
                #
                #     # 方向
                #     dire = (sp2.x - ep2.x)
                #
                #     # 计算夹角
                # else:
                #     last_arc = last_arc_list[conn[0]]
                #     # 圆弧中心 上一个Arc的center与上一个Arc末端点的连线与当前path_seg的中垂线的交点
                #     croter_line = Segment2(last_arc.center, last_arc.get_pos(1.0)).line
                #     # 判断平行
                #     if croter_line.is_parallel(path_seg.perpendicular_bisector):
                #         # 特殊处理，这种情况极其少见，但是不排除
                #         cp2 = path_seg.center
                #     else:
                #         cp2 = croter_line.get_intersection(path_seg.perpendicular_bisector)
                #
                #     # 方向 以起始音符为起点，终止音符和上一个圆心为终点，构建两个向量，夹角为钝角则较上次反，锐角则同上次，直角特殊处理
                #     deter_seg = Segment2(last_arc.center, last_arc.get_pos(1.0))  # 末角向量/判定线
                #
                #     if path_seg.perpendicular_bisector.is_parallel(deter_seg.line):
                #         # 特殊处理，这种情况极其少见，但是不排除
                #         dire = 0
                #     else:
                #         v1 = sp2.get_vector2(last_arc.center)
                #         v2 = sp2.get_vector2(ep2)
                #         if v1.get_angle(v2) > math.pi / 2:
                #             dire = -1 * last_arc.direction
                #         else:
                #             dire = last_arc.direction
                # sv2, ev2 = cp2.get_vector2(sp2), cp2.get_vector2(ep2)  # 起始和结束点对于圆心的向量
                # try:
                #     radian = sv2.get_angle(ev2)  # 弧度
                # except ZeroDivisionError:
                #     radian = 10
                # radius = Segment2(cp2, sp2).length  # 半径
                # arc2 = Arc2(cp2, radius, sv2.get_angle(Vector2(1, 0)), ev2.get_angle(Vector2(1, 0)), dire)   # 生成Arc2
                # this_arc_list.append(arc2)
                # pl = arc22pl(arc2)  # 生成ParticleLine
                # lines.append(pl)
            last_arc_list = this_arc_list
        return lines
