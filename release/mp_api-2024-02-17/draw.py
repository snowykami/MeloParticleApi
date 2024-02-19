from typing import Tuple


class Color:
    def __init__(self, color: Tuple[int, int, int, int] | int | str | Tuple[int, int, int]):
        """Initialize a Color object.

        Args:
            color (Tuple[int, int, int, int] | int | str | Tuple[int, int, int]):
                - Tuple[int, int, int, int]: Represents ARGB values (alpha, red, green, blue).
                - int: Represents an integer color value.
                - str: Represents a hexadecimal color string.
                - Tuple[int, int, int]: Represents RGB values (red, green, blue).
        """
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
        """Get the integer representation of the color.

        Args:
            alpha (bool, optional): Whether to include the alpha channel. Defaults to False.

        Returns:
            int: Integer representation of the color.
        """
        if alpha:
            return (self.a << 24) + (self.r << 16) + (self.g << 8) + self.b
        else:
            return (self.r << 16) + (self.g << 8) + self.b

    def get_hex(self, alpha: bool = True, hashtag: bool = True) -> str:
        """Get the hexadecimal representation of the color.

        Args:
            alpha (bool, optional): Whether to include the alpha channel. Defaults to True.
            hashtag (bool, optional): Whether to include '#' in the hexadecimal string.

        Returns:
            str: Hexadecimal representation of the color.
        """
        if alpha:
            return ("#" if hashtag else "") + hex(self.a)[2:].rjust(2, '0') + hex(self.r)[2:].rjust(2, '0') + hex(self.g)[2:].rjust(2, '0') + hex(self.b)[2:].rjust(2, '0')
        else:
            return ("#" if hashtag else "") + hex(self.r)[2:].rjust(2, '0') + hex(self.g)[2:].rjust(2, '0') + hex(self.b)[2:].rjust(2, '0')

    def get_tuple(self, alpha: bool = True) -> Tuple[int, int, int] | Tuple[int, int, int, int]:
        """Get the color values as a tuple.

        Args:
            alpha (bool, optional): Whether to include the alpha channel. Defaults to True.

        Returns:
            Tuple[int, int, int] | Tuple[int, int, int, int]: Color values as a tuple.
        """
        if alpha:
            return self.argb
        else:
            return self.argb[1:]

    def gradient_interpolation_rgba(self, other: 'Color', p: float) -> 'Color':
        """Perform linear color interpolation for creating a gradient color.

        Args:
            other (Color): Another color for interpolation.
            p (float): Interpolation coefficient in the range [0, 1].

        Returns:
            Color: Interpolated color.
        """
        return Color((
                int(self.a + (other.a - self.a) * p),
                int(self.r + (other.r - self.r) * p),
                int(self.g + (other.g - self.g) * p),
                int(self.b + (other.b - self.b) * p)
        ))

    def gradient_interpolation(self, other: 'Color', p: float) -> 'Color':
        """Perform linear color interpolation for creating a gradient color.

        Args:
            other (Color): Another color for interpolation.
            p (float): Interpolation coefficient in the range [0, 1].

        Returns:
            Color: Interpolated color.
        """
        return self.gradient_interpolation_rgba(other, p)

    def __str__(self) -> str:
        """Return a string representation of the Color object."""
        return f'Color {self.get_hex}'

    def __add__(self, other: 'Color') -> 'Color':
        """Perform addition of two colors.

        Args:
            other (Color): Another color to add.

        Returns:
            Color: Result of the addition.
        """
        result_r = min(self.r + other.r, 255)
        result_g = min(self.g + other.g, 255)
        result_b = min(self.b + other.b, 255)
        result_a = min(self.a + other.a, 255)
        return Color((result_a, result_r, result_g, result_b))

    def __sub__(self, other: 'Color') -> 'Color':
        """Perform subtraction of two colors.

        Args:
            other (Color): Another color to subtract.

        Returns:
            Color: Result of the subtraction.
        """
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
