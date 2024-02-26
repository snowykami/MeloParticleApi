from mp_api.typing import T_Num


class Point2:
    """表示二维空间中的点。

    Attributes:
        x (T_Num): x坐标。
        y (T_Num): y坐标。
    """

    def __init__(self, x: T_Num, y: T_Num):
        """使用给定的坐标初始化一个新的Point2。

        Args:
            x (T_Num): x坐标。
            y (T_Num): y坐标。
        """
        self.x = x
        self.y = y

    def __str__(self):
        """返回点的字符串表示。

        Returns:
            str: 一个格式为'Point2: (x, y)'的字符串。
        """
        return f"Point2: ({self.x}, {self.y})"


class Point3:
    """表示三维空间中的点。

    Attributes:
        x (T_Num): x坐标。
        y (T_Num): y坐标。
        z (T_Num): z坐标。
    """

    def __init__(self, x: T_Num, y: T_Num, z: T_Num):
        """使用给定的坐标初始化一个新的Point3。

        Args:
            x (T_Num): x坐标。
            y (T_Num): y坐标。
            z (T_Num): z坐标。
        """

        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        """返回点的字符串表示。

        Returns:
            str: 一个格式为'Point3: (x, y, z)'的字符串。
        """
        return f"Point3: ({self.x}, {self.y}, {self.z})"


class Line2:
    """表示二维空间中的直线。

    Attributes:
        a (T_Num): x的系数。
        b (T_Num): y的系数。
        c (T_Num): 常数项。
    """

    def __init__(self, a: T_Num, b: T_Num, c: T_Num):
        """使用给定的系数初始化一个新的Line2。

        Args:
            a (T_Num): x的系数。
            b (T_Num): y的系数。
            c (T_Num): 常数项。
        """
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        """返回直线的字符串表示。

        Returns:
            str: 一个格式为'Line2: ax + by + c = 0'的字符串。
        """
        return f"Line2: {self.a}x + {self.b}y + {self.c} = 0"


class Line3:
    """表示三维空间中的直线。

    Attributes:
        a (T_Num): x的系数。
        b (T_Num): y的系数。
        c (T_Num): z的系数。
        d (T_Num): 常数项。
    """

    def __init__(self, a: T_Num, b: T_Num, c: T_Num, d: T_Num):
        """使用给定的系数初始化一个新的Line3。

        Attributes:
            a (T_Num): x的系数。
            b (T_Num): y的系数。
            c (T_Num): z的系数。
            d (T_Num): 常数项。
        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __str__(self):
        """返回直线的字符串表示。

        Returns:
            str: 一个格式为'Line3: ax + by + cz + d = 0'的字符串。
        """
        return f"Line3: {self.a}x + {self.b}y + {self.c}z + {self.d} = 0"


class Segment2:
    """表示二维空间中的线段。

    Attributes
        p1 (Point2): 起点。
        p2 (Point2): 终点。
    """

    def __init__(self, p1: Point2, p2: Point2):
        """使用给定的起点和终点初始化一个新的Segment2。

        Args:
            p1 (Point2): 起点。
            p2 (Point2): 终点。
        """
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        """返回线段的字符串表示。

        Returns:
            str: 一个格式为'Segment2: (x1, y1) -> (x2, y2)'的字符串。
        """

        return f"Segment2: {self.p1} -> {self.p2}"


class Segment3:
    """表示三维空间中的线段。

    Attributes:
        p1 (Point3): 起点。
        p2 (Point3): 终点。
    """

    def __init__(self, p1: Point3, p2: Point3):
        """使用给定的起点和终点初始化一个新的Segment3。

        Args:
            p1 (Point3): 起点。
            p2 (Point3): 终点。
        """
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        """返回线段的字符串表示。

        Returns:
            str: 一个格式为'Segment3: (x1, y1, z1) -> (x2, y2, z2)'的字符串。
        """
        return f"Segment3: {self.p1} -> {self.p2}"


class Vector2:
    """表示二维空间中的向量。

    Attributes:
        x (T_Num): x分量。
        y (T_Num): y分量。
    """

    def __init__(self, x: T_Num, y: T_Num):
        """使用给定的分量初始化一个新的Vector2。

        Args:
            x (T_Num): x分量。
            y (T_Num): y分量。
        """
        self.x = x
        self.y = y

    def __str__(self):
        """返回向量的字符串表示。

        Returns:
            str: 一个格式为'Vector2: (x, y)'的字符串。
        """
        return f"Vector2: ({self.x}, {self.y})"


class Vector3:
    """表示三维空间中的向量。

    Attributes:
        x (T_Num): x分量。
        y (T_Num): y分量。
        z (T_Num): z分量。
    """

    def __init__(self, x: T_Num, y: T_Num, z: T_Num):
        """使用给定的分量初始化一个新的Vector3。

        Args:
            x (T_Num): x分量。
            y (T_Num): y分量。
            z (T_Num): z分量。
        """
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        """返回向量的字符串表示。

        Returns:
            str: 一个格式为'Vector3: (x, y, z)'的字符串。
        """
        return f"Vector3: ({self.x}, {self.y}, {self.z})"


class VectorN:
    """表示n维空间中的向量。

    Attributes:
        data (Tuple[T_Num]): 向量的分量。
    """

    def __init__(self, *args: T_Num):
        """使用给定的分量初始化一个新的VectorN。

        Args:
            *args (T_Num): 向量的分量。
        """
        self.data = args

    def __str__(self):
        """返回向量的字符串表示。

        Returns:
            str: 一个格式为'VectorN: (x1, x2, ..., xn)'的字符串。
        """
        return f"Vector{len(self.data)}: {self.data}"
