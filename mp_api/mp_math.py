import math

from mp_api import T_Num


class Note:
    def __init__(self,
                 start,
                 end,
                 note,
                 velocity
                 ):
        self.start = start
        self.end = end
        self.note = note
        self.velocity = velocity


class Point2:
    def __init__(self,
                 x,
                 y
                 ):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point2({self.x}, {self.y})"

    def get_vector2(self, p: 'Point2') -> 'Vector2':
        """
        Get the vector of two points
        :param p: 指向的点
        :return:
        """
        return Vector2(p.x - self.x, p.y - self.y)


class Point3:
    def __init__(self,
                 x,
                 y,
                 z
                 ):
        self.x = x
        self.y = y
        self.z = z
        self.t = 0

    @property
    def point2mc(self):
        return Point2(self.x, self.z)

    def __str__(self):
        return f"Point3({self.x}, {self.y}, {self.z})"


class Line2:
    def __init__(self,
                 a,
                 b,
                 c
                 ):
        self.a = a
        self.b = b
        self.c = c

    def get_parallel_line(self,
                          point: 'Point2'
                          ):
        """
        Get the parallel line of the line
        :param point: outside point
        :return:
        """
        return Line2(
            a=self.a,
            b=self.b,
            c=self.a * point.x + self.b * point.y
        )

    def get_intersection(self, line: 'Line2') -> Point2:
        """
        Get the intersection of two lines
        :param line: another line
        :return: intersection point
        """
        if self.a * line.b == self.b * line.a:
            raise ValueError('No intersection')
        d = self.a * line.b - self.b * line.a
        return Point2(
            (self.b * line.c - self.c * line.b) / d,
            (self.c * line.a - self.a * line.c) / d
        )

    def get_perpendicular_line(self,
                               point: 'Point2'
                               ):
        """
        Get the perpendicular line of the line
        :param point: outside point
        :return:
        """
        return Line2(
            a=-self.b,
            b=self.a,
            c=self.b * point.x - self.a * point.y
        )

    def is_parallel(self, line: 'Line2') -> bool:
        """
        Check if two lines are parallel
        :param line: another line
        :return: True if parallel
        """
        return self.a * line.b == self.b * line.a


class Line3:
    def __init__(self,
                 a,
                 b,
                 c,
                 d
                 ):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def get_parallel_line(self,
                          p: 'Point3'
                          ):
        return Line3(self.a, self.b, self.c, self.a * p.x + self.b * p.y + self.c * p.z)


class Segment2:
    def __init__(self,
                 start: Point2,
                 end: Point2
                 ):
        self.start = start
        self.end = end

    @property
    def line(self):
        """
        Get the line of the segment
        :return: 线段所在的直线
        """
        return Line2(
            a=self.end.y - self.start.y,
            b=self.start.x - self.end.x,
            c=self.end.x * self.start.y - self.start.x * self.end.y
        )

    @property
    def center(self):
        """
        Get the center of the segment
        :return: 线段的中点
        """
        return Point2(
            (self.start.x + self.end.x) / 2,
            (self.start.y + self.end.y) / 2
        )

    @property
    def length(self):
        """
        Get the length of the segment
        :return: 线段的长度
        """
        return ((self.start.x - self.end.x) ** 2 + (self.start.y - self.end.y) ** 2) ** 0.5

    @property
    def perpendicular_bisector(self):
        """
        Get the perpendicular bisector of the segment
        :return: 线段的中垂线
        """
        return self.line.get_perpendicular_line(self.center)

    def is_point_at(self, point: Point2) -> bool:
        """
        Check if the point is on the segment
        :param point: another point
        :return: True if the point is on the segment
        """
        return (self.start.x - point.x) * (self.end.x - point.x) <= 0 and (self.start.y - point.y) * (self.end.y - point.y) <= 0


class Arc2:
    def __init__(self,
                 center: Point2,
                 radius: T_Num,
                 start: Point2,
                 end: Point2,
                 direction: int = 1
                 ):
        """

        :param center: 处理特殊情况
        :param radius:
        :param start: 起点向量末端点
        :param end: 终点向量末端点
        :param direction: 正数为正角，负数为负角，0为零角，数值绝对值与方向无关
        """
        self.center = center
        self.radius = radius
        self.start = start
        self.end = end
        self.direction = direction
        # 正负角方向
        if self.direction != 0:
            self.direction = self.direction / abs(self.direction)

    def get_pos(self, p: T_Num) -> Point2:
        """
        获取当前旋转进度的坐标
        Get the position of the arc
        :param p: 0-1
        :return:
        """
        v1 = self.center.get_vector2(self.start)
        v2 = self.center.get_vector2(self.end)
        # 要计算正负角
        angle1 = math.atan2(v1.y, v1.x)
        angle2 = math.atan2(v2.y, v2.x)

        # 计算两个角度之间的差值
        delta_angle = angle2 - angle1

        # 根据旋转方向调整差值
        if self.direction > 0:
            if delta_angle < 0:
                delta_angle += 2 * math.pi
        else:
            if delta_angle > 0:
                delta_angle -= 2 * math.pi

        return Point2(
            self.center.x + self.radius * math.cos(angle1 + delta_angle * p),
            self.center.y + self.radius * math.sin(angle1 + delta_angle * p)
        )

    def get_tangent(self, p: T_Num) -> Line2:
        """
        获取当前进度位置的切线
        Get the tangent of the arc
        :param p: 0-1 进度系数，不是点
        :return:
        """

        point = self.get_pos(p)
        radius_seg = Segment2(self.center, point)
        return radius_seg.line.get_perpendicular_line(point)


class Vector2:
    def __init__(self,
                 x,
                 y
                 ):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector2({self.x}, {self.y})"

    def get_angle(self, vector2: 'Vector2') -> T_Num:
        """
        Get the angle of two vectors
        :param vector2: another vector
        :return: angle in radian
        """
        if self.length == 0 or vector2.length == 0:
            print(self, vector2)
        cos = (self * vector2 / (self.length * vector2.length))

        return math.cos(clamp(cos, -1, 1))

    @property
    def length(self):
        """
        Get the length of the vector
        :return: length
        """
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __add__(self, other: 'Vector2'):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2'):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: T_Num | type('Vector2')):
        if isinstance(other, Vector2):
            return self.x * other.x + self.y * other.y
        else:
            return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other: T_Num):
        return Vector2(self.x / other, self.y / other)

    def __neg__(self):
        return Vector2(-self.x, -self.y)


class Vector3:
    def __init__(self,
                 x,
                 y,
                 z
                 ):
        self.x = x
        self.y = y
        self.z = z


def line2by2p(p1: Point2, p2: Point2) -> Line2:
    """
    Get the line of two points
    :param p1:
    :param p2:
    :return:
    """
    return Line2(
        a=p2.y - p1.y,
        b=p1.x - p2.x,
        c=p2.x * p1.y - p1.x * p2.y
    )


def clamp(_x: T_Num, _min: T_Num, _max: T_Num) -> T_Num:
    return _min if _x < _min else _max if _x > _max else _x
