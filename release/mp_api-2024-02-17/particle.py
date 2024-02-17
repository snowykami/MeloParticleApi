from .mp_typing import T_Exp, T_Color
from .utils import func2math_exp
from typing import Callable


class BaseParticle:
    def __init__(self, name: str = ''):
        """
        代表粒子的基础类。

        参数：
        - name (str): 粒子的名称。
        """
        self._name = name

    @property
    def name(self) -> str:
        """
        获取粒子的名称。

        返回：
        str: 粒子的名称。
        """
        return self._name


class BestParticle(BaseParticle):
    def __init__(
            self,
            x_exp: T_Exp = lambda t: 0,
            y_exp: T_Exp = lambda t: 0,
            z_exp: T_Exp = lambda t: 0,
            life: int = 1,
            rand: int = 1,
            color: T_Exp | T_Color = 'white'
    ):
        super().__init__()
        self.x_exp = func2math_exp(x_exp)
        self.y_exp = func2math_exp(y_exp)
        self.z_exp = func2math_exp(z_exp)
        self.life = life
        assert rand > 0, "rand must be greater than 0"
        self.rand = rand
        if isinstance(color, Callable):
            self.color = func2math_exp(color)
        else:
            self.color = color

    @property
    def name(self) -> str:
        """
        获取粒子的名称字符串。

        返回：
        str: 粒子的名称字符串。
        """
        return f"soy:best '{self.x_exp}' '{self.y_exp}' '{self.z_exp}' {self.life} {self.rand} '{self.color}'"


class ColorLifeParticle(BaseParticle):
    def __init__(self,
                 color: T_Color = 'white',
                 life: int = 1,
                 rand: int = 1
                 ):
        super().__init__()
        self.color = color
        self.life = life
        self.rand = rand

    @property
    def name(self) -> str:
        """
        获取粒子的名称字符串。

        返回：
        str: 粒子的名称字符串。
        """
        return f"soy:life_color_particle {self.color} {self.life} {self.rand}"


class ColorLifeScaleTextureParticle(BaseParticle):
    def __init__(
            self,
            color: T_Color = 'white',
            life: int = 1,
            rand: int = 1,
            scale: float = 1.0,
            texture: str = 'minecraft:particle'
    ):
        super().__init__()
        self.color = color
        self.life = life
        self.rand = rand
        self.scale = scale
        self.texture = texture

    @property
    def name(self) -> str:
        """
        获取粒子的名称字符串。

        返回：
        str: 粒子的名称字符串。
        """
        return f"soy:life_color_texture {self.color} {self.life} {self.rand} {self.scale} '{self.texture}'"


class SeqParticle(BaseParticle):
    def __init__(self,
                 x_list: list,
                 y_list: list,
                 z_list: list,
                 life: int = 1,
                 rand: int = 1,
                 color_list: list = None,
                 scale_list: list = None
                 ):
        super().__init__()
        self.x_list = x_list
        self.y_list = y_list
        self.z_list = z_list
        self.life = life
        self.rand = rand
        self.color_list = color_list
        self.scale_list = scale_list

    @property
    def name(self) -> str:
        """
        获取粒子的名称字符串。

        返回：
        str: 粒子的名称字符串。
        """
        return f"soy:seq {self.x_list} {self.y_list} {self.z_list} {self.life} {self.rand} {self.color_list} {self.scale_list}"


class SeqtParticle(BaseParticle):
    def __init__(self,
                 x_list: list,
                 y_list: list,
                 z_list: list,
                 life: int = 1,
                 rand: int = 1,
                 color_list: list = None,
                 scale_list: list = None,
                 texture: str = 'minecraft:particle'
                 ):
        super().__init__()
        self.x_list = x_list
        self.y_list = y_list
        self.z_list = z_list
        self.life = life
        self.rand = rand
        self.color_list = color_list
        self.scale_list = scale_list
        self.texture = texture

    @property
    def name(self) -> str:
        """
        获取粒子的名称字符串。

        返回：
        str: 粒子的名称字符串。
        """
        return f"soy:seqt {self.x_list} {self.y_list} {self.z_list} {self.life} {self.rand} {self.color_list} {self.scale_list} '{self.texture}'"
