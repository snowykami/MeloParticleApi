import math
from typing import List

import numpy as np
from .mp_typing import T_Num


class Note:
    def __init__(self, start, end, note, velocity):
        """
        Initialize a Note object.

        Args:
            start: Start time of the note.
            end: End time of the note.
            note: Note value.
            velocity: Velocity of the note.
        """
        self.start = start
        self.end = end
        self.note = note
        self.velocity = velocity


class Point2:
    def __init__(self, x, y):
        """
        Initialize a 2D point.

        Args:
            x: X-coordinate.
            y: Y-coordinate.
        """
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point2({self.x}, {self.y})"

    def get_vector2(self, p: 'Point2') -> 'Vector2':
        """
        Get the vector from the current point to another point.

        Args:
            p: Another Point2 object.

        Returns:
            Vector2: Vector from the current point to the specified point.
        """
        return Vector2(p.x - self.x, p.y - self.y)

    def get_distance(self, point: 'Point2') -> T_Num:
        """
        Get the Euclidean distance between two points.

        Args:
            point: Another Point2 object.

        Returns:
            T_Num: Euclidean distance between the points.
        """
        return ((self.x - point.x) ** 2 + (self.y - point.y) ** 2) ** 0.5


class Point3:
    def __init__(self, x, y, z, t=0):
        """
        Initialize a 3D point.

        Args:
            x: X-coordinate.
            y: Y-coordinate.
            z: Z-coordinate.
        """
        self.x = x
        self.y = y
        self.z = z
        self.t = 0

    @property
    def point2mc(self):
        """
        Convert the 3D point to a 2D point (ignoring the y-coordinate).

        Returns:
            Point2: 2D point representation of the 3D point.
        """
        return Point2(self.x, self.z)

    def get_distance(self, point: 'Point3') -> T_Num:
        """
        Get the Euclidean distance between two points.

        Args:
            point: Another Point3 object.

        Returns:
            T_Num: Euclidean distance between the points.
        """
        return ((self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2) ** 0.5

    def __str__(self):
        return f"Point3({self.x}, {self.y}, {self.z})"


class Line2:
    def __init__(self, a, b, c):
        """
        Initialize a 2D line.

        Args:
            a: Coefficient of x in the line equation.
            b: Coefficient of y in the line equation.
            c: Constant term in the line equation.
        """
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return f"Line2({self.a}, {self.b}, {self.c})"

    def get_parallel_line(self, point: 'Point2'):
        """
        Get the parallel line passing through a specified point.

        Args:
            point: A Point2 object.

        Returns:
            Line2: Parallel line passing through the specified point.
        """
        return Line2(a=self.a, b=self.b, c=self.a * point.x + self.b * point.y)

    def get_intersection(self, line: 'Line2') -> Point2:
        """
        Get the intersection point with another Line2 object.

        Args:
            line: Another Line2 object.

        Returns:
            Point2: Intersection point.
        """
        if self.a * line.b == self.b * line.a:
            raise ValueError('No intersection')
        d = self.a * line.b - self.b * line.a
        return Point2((self.b * line.c - self.c * line.b) / d, (self.c * line.a - self.a * line.c) / d)

    def get_perpendicular_line(self, point: 'Point2'):
        """
        Get the perpendicular line passing through a specified point.

        Args:
            point: A Point2 object.

        Returns:
            Line2: Perpendicular line passing through the specified point.
        """
        return Line2(a=-self.b, b=self.a, c=self.b * point.x - self.a * point.y)

    def is_parallel(self, line: 'Line2') -> bool:
        """
        Check if two lines are parallel.

        Args:
            line: Another Line2 object.

        Returns:
            bool: True if the lines are parallel.
        """
        return self.a * line.b == self.b * line.a


class Line3:
    def __init__(self, a, b, c, d):
        """
        Initialize a 3D line.

        Args:
            a: Coefficient of x in the line equation.
            b: Coefficient of y in the line equation.
            c: Coefficient of z in the line equation.
            d: Constant term in the line equation.
        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def get_parallel_line(self, p: 'Point3'):
        """
        Get the parallel line passing through a specified 3D point.

        Args:
            p: A Point3 object.

        Returns:
            Line3: Parallel line passing through the specified point.
        """
        return Line3(self.a, self.b, self.c, self.a * p.x + self.b * p.y + self.c * p.z)


class Segment2:
    def __init__(self, start: Point2, end: Point2):
        """
        Initialize a 2D line segment.

        Args:
            start: Start Point2 of the segment.
            end: End Point2 of the segment.
        """
        self.start = start
        self.end = end

    @property
    def line(self):
        """
        Get the Line2 object representing the line of the segment.

        Returns:
            Line2: Line object representing the segment.
        """
        return Line2(a=self.end.y - self.start.y, b=self.start.x - self.end.x, c=self.end.x * self.start.y - self.start.x * self.end.y)

    @property
    def center(self):
        """
        Get the center Point2 of the segment.

        Returns:
            Point2: Center of the segment.
        """
        return Point2((self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2)

    @property
    def length(self):
        """
        Get the length of the segment.

        Returns:
            T_Num: Length of the segment.
        """
        return ((self.start.x - self.end.x) ** 2 + (self.start.y - self.end.y) ** 2) ** 0.5

    @property
    def perpendicular_bisector(self):
        """
        Get the Line2 object representing the perpendicular bisector of the segment.

        Returns:
            Line2: Perpendicular bisector of the segment.
        """
        return self.line.get_perpendicular_line(self.center)

    def is_point_at(self, point: Point2) -> bool:
        """
        Check if a point is on the segment.

        Args:
            point: A Point2 object.

        Returns:
            bool: True if the point lies on the segment.
        """
        return (self.start.x - point.x) * (self.end.x - point.x) <= 0 and (self.start.y - point.y) * (self.end.y - point.y) <= 0


class Arc2:
    def __init__(self, center: Point2 | None, start: Point2, end: Point2, direction: int = 1):
        """
        Initialize a 2D arc.

        Args:
            center: Center Point2 of the arc. If None, the arc is a straight line.
            start: Start Point2 of the arc.
            end: End Point2 of the arc.
            direction: Positive for positive angles, negative for negative angles, 0 for zero angles (independent of direction).
        """
        self.center = center
        self.radius = center.get_vector2(start).length if center is not None else 0
        self.start = start
        self.end = end
        self.direction = direction
        # Ensure positive/negative direction
        if self.direction != 0:
            self.direction = self.direction / abs(self.direction)

    def get_delta_angle(self) -> T_Num:
        """
        Get the angular difference, including positive/negative angles.

        Returns:
            T_Num: Angular difference.
        """
        v1 = self.center.get_vector2(self.start)
        v2 = self.center.get_vector2(self.end)
        # Calculate positive/negative angles
        angle1 = math.atan2(v1.y, v1.x)
        angle2 = math.atan2(v2.y, v2.x)

        # Calculate angular difference
        delta_angle = angle2 - angle1

        # Adjust the difference based on rotation direction
        if self.direction > 0:
            if delta_angle < 0:
                delta_angle += 2 * math.pi
        else:
            if delta_angle > 0:
                delta_angle -= 2 * math.pi
        return delta_angle

    def get_points(self, density: T_Num = 0.1) -> List[Point2]:
        """
        获取沿弧等间隔的坐标，使用numpy。

        Args:
            density (T_Num): 点的密度。

        Returns:
            np.ndarray: Array of coordinates at equal intervals along the arc.
        """
        # 生成一个表示进度的数组
        p = np.linspace(0, 1, int(self.length / density))

        # 计算每个进度的角度
        v1 = self.center.get_vector2(self.start)
        angle1 = math.atan2(v1.y, v1.x)
        delta_angle = self.get_delta_angle()

        # Adjust the difference based on rotation direction
        if self.direction > 0:
            if delta_angle < 0:
                delta_angle += 2 * math.pi
        else:
            if delta_angle > 0:
                delta_angle -= 2 * math.pi

        # 使用numpy的cos和sin函数批量计算每个进度的坐标
        x = self.center.x + self.radius * np.cos(angle1 + delta_angle * p)
        y = self.center.y + self.radius * np.sin(angle1 + delta_angle * p)

        return [Point2(x[i], y[i]) for i in range(len(x))]

    def get_pos(self, p: T_Num) -> Point2:
        """
        Get the coordinates at the current rotation progress.

        Args:
            p: Rotation progress coefficient in the range [0, 1].

        Returns:
            Point2: Coordinates at the specified rotation progress.
        """
        v1 = self.center.get_vector2(self.start)
        angle1 = math.atan2(v1.y, v1.x)
        delta_angle = self.get_delta_angle()

        # Adjust the difference based on rotation direction
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

    @property
    def length(self) -> T_Num:
        """
        Get the arc length.

        Returns:
            T_Num: Arc length.
        """
        delta_angle = self.get_delta_angle()

        # Adjust the difference based on rotation direction
        if self.direction > 0:
            if delta_angle < 0:
                delta_angle += 2 * math.pi
        else:
            if delta_angle > 0:
                delta_angle -= 2 * math.pi

        return self.radius * abs(delta_angle)

    def get_vector2(self, p: T_Num) -> 'Vector2':
        """
        Get the tangent vector at the current rotation progress.

        Args:
            p: Rotation progress coefficient in the range [0, 1].

        Returns:
            Vector2: Tangent vector at the specified rotation progress.
        """
        v1 = self.center.get_vector2(self.start)
        angle1 = math.atan2(v1.y, v1.x)
        delta_angle = self.get_delta_angle()

        # Adjust the difference based on rotation direction
        if self.direction > 0:
            if delta_angle < 0:
                delta_angle += 2 * math.pi
        else:
            if delta_angle > 0:
                delta_angle -= 2 * math.pi

        return Vector2(
            -self.radius * math.sin(angle1 + delta_angle * p),
            self.radius * math.cos(angle1 + delta_angle * p)
        )


class Vector2:
    def __init__(self, x, y):
        """
        Initialize a 2D vector.

        Args:
            x: X-component.
            y: Y-component.
        """
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector2({self.x}, {self.y})"

    def get_angle(self, vector2: 'Vector2') -> T_Num:
        """
        Get the angle between two vectors.

        Args:
            vector2: Another Vector2 object.

        Returns:
            T_Num: Angle in radians.
        """
        return math.acos(self * vector2 / (self.length * vector2.length))

    @property
    def length(self):
        """
        Get the length of the vector.

        Returns:
            T_Num: Length of the vector.
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
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def line2by2p(p1: Point2, p2: Point2) -> Line2:
    """
    Get the Line2 object passing through two points.

    Args:
        p1: First Point2.
        p2: Second Point2.

    Returns:
        Line2: Line object passing through the specified points.
    """
    return Line2(
        a=p2.y - p1.y,
        b=p1.x - p2.x,
        c=p2.x * p1.y - p1.x * p2.y
    )


def clamp(_x: T_Num, _min: T_Num, _max: T_Num) -> T_Num:
    """
    Clamp a value within a specified range.

    Args:
        _x: Value to be clamped.
        _min: Minimum allowed value.
        _max: Maximum allowed value.

    Returns:
        T_Num: Clamped value.
    """
    return _min if _x < _min else _max if _x > _max else _x
