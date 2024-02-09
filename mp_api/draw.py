from typing import Tuple
from .mp_typing import T_RGB, T_ARGB, T_Color


class Color:
    def __init__(self, color: T_Color | 'Color'):
        """
        :param color: 16777215+(FF,16) | (#)(FF)FFFFFF | (255, 255, 255) | (255, 255, 255, 255)
        """
        # 统一储存为Tuple[int a, int r, int g, int b]
        # 判断argb和rgb，若没有a则a为255
        if isinstance(color, Color):
            self.argb = color.argb
        elif isinstance(color, int):
            if color >= 16777216:
                self.argb = (color >> 24 & 0xFF, color >> 16 & 0xFF, color >> 8 & 0xFF, color & 0xFF)
            else:
                self.argb = (255, color >> 16 & 0xFF, color >> 8 & 0xFF, color & 0xFF)
        elif isinstance(color, str):
            if color[0] == '#':
                color = color[1:]
            if len(color) == 6:
                self.argb = (255, int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16))
            elif len(color) == 8:
                self.argb = (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16), int(color[6:8], 16))
            else:
                raise ValueError("Color format error")
        elif isinstance(color, tuple):
            if len(color) == 3:
                self.argb = (255, color[0], color[1], color[2])
            elif len(color) == 4:
                self.argb = color
            else:
                raise ValueError("Color format error")
        else:
            raise ValueError("Color format error")

        self.a = self.argb[0]
        self.r = self.argb[1]
        self.g = self.argb[2]
        self.b = self.argb[3]

    def get_int(self, alpha: bool = False) -> int:
        """获取整数颜色
        :param alpha: 是否包含alpha通道，默认否
        :return: 整数颜色
        """
        if alpha:
            return (self.a << 24) + (self.r << 16) + (self.g << 8) + self.b
        else:
            return (self.r << 16) + (self.g << 8) + self.b

    def get_hex(self, alpha: bool = True, hashtag: bool = True) -> str:
        """获取十六进制颜色
        :param alpha: 是否包含alpha通道，默认是
        :param hashtag: 是否包含#
        :return: 十六进制颜色
        """
        if alpha:
            return ("#" if hashtag else "") + hex(self.a)[2:].rjust(2, '0') + hex(self.r)[2:].rjust(2, '0') + hex(self.g)[2:].rjust(2, '0') + hex(self.b)[2:].rjust(2, '0')
        else:
            return ("#" if hashtag else "") + hex(self.r)[2:].rjust(2, '0') + hex(self.g)[2:].rjust(2, '0') + hex(self.b)[2:].rjust(2, '0')

    def get_tuple(self, alpha: bool = True) -> T_RGB | T_ARGB:
        """获取颜色元组
        :param alpha: 是否包含alpha通道，默认是
        :return: 颜色数组
        """
        if alpha:
            return self.argb
        else:
            return self.argb[1:]

    def gradient_interpolation(self, other: 'Color', p: float) -> 'Color':
        """使用线性颜色插值计算渐变色
        :param other: 另一个颜色
        :param p: 插值系数
        :return: 插值颜色
        """
        return Color((
            int(self.a + (other.a - self.a) * p),
            int(self.r + (other.r - self.r) * p),
            int(self.g + (other.g - self.g) * p),
            int(self.b + (other.b - self.b) * p)
        ))

    def __str__(self):
        return f'Color {self.get_hex}'

    def __add__(self, other: 'Color'):
        result_r = min(self.r + other.r, 255)
        result_g = min(self.g + other.g, 255)
        result_b = min(self.b + other.b, 255)
        result_a = min(self.a + other.a, 255)
        return Color((result_a, result_r, result_g, result_b))

    def __sub__(self, other: 'Color'):
        result_r = max(self.r - other.r, 0)
        result_g = max(self.g - other.g, 0)
        result_b = max(self.b - other.b, 0)
        result_a = max(self.a - other.a, 0)
        return Color((result_a, result_r, result_g, result_b))


class CColor:
    # Constants Color
    WHITE = Color("#FFFFFF")
    BLACK = Color("#000000")
    RED = Color("#FF0000")
    GREEN = Color("#00FF00")
    BLUE = Color("#0000FF")
    YELLOW = Color("#FFFF00")
    CYAN = Color("#00FFFF")
    MAGENTA = Color("#FF00FF")
    ORANGE = Color("#FFA500")
    PURPLE = Color("#800080")
    GRAY = Color("#808080")
    LIGHT_GRAY = Color("#D3D3D3")