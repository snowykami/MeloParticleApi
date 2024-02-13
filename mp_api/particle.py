from .mp_typing import *
from .draw import Color, CColor
from .utils import *


class BaseParticle(object):
    def __init__(self, name: str = ''):
        self._name = name

    @property
    def name(self):
        return self._name


class BestParticle(BaseParticle):
    def __init__(
            self,
            x_exp: T_Exp = lambda t: 0,
            y_exp: T_Exp = lambda t: 0,
            z_exp: T_Exp = lambda t: 0,
            life: int = 1,
            rand: int = 1,
            color: T_Exp | T_Color = str(CColor.WHITE.get_int())
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
            self.color = Color(color).get_int()

    @property
    def name(self):
        return f"soy:best '{self.x_exp}' '{self.y_exp}' '{self.z_exp}' {self.life} {self.rand} '{self.color}'"


class ColorLifeParticle(BaseParticle):

    def __init__(self,
                 color: T_Color = CColor.WHITE,
                 life: int = 1,
                 rand: int = 1
                 ):
        super().__init__()
        self.color = Color(color)
        self.life = life
        self.rand = rand

    @property
    def name(self):
        return f"soy:life_color_particle {self.color.get_int()} {self.life} {self.rand}"


class ColorLifeScaleTextureParticle(BaseParticle):

    def __init__(
            self,
            color: T_Color = CColor.WHITE,
            life: int = 1,
            rand: int = 1,
            scale: T_Num = 1.0,
            texture: str = 'minecraft:particle'
    ):
        super().__init__()
        self.color = Color(color)
        self.life = life
        self.rand = rand
        self.scale = scale
        self.texture = texture

    @property
    def name(self):
        return f"soy:life_color_texture {self.color.get_int()} {self.life} {self.rand} {self.scale} '{self.texture}'"


class SeqParticle(BaseParticle):
    def __init__(self,
                 x_list: List[T_Num,],
                 y_list: List[T_Num,],
                 z_list: List[T_Num,],
                 life: int = 1,
                 rand: int = 1,
                 color_list=List[T_Color,],
                 scale_list=List[T_Num,]
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
    def name(self):
        return f"soy:seq {self.x_list} {self.y_list} {self.z_list} {self.life} {self.rand} {self.color_list} {self.scale_list}"


class SeqtParticle(BaseParticle):
    def __init__(self,
                 x_list: List[T_Exp,],
                 y_list: List[T_Exp,],
                 z_list: List[T_Exp,],
                 life: int = 1,
                 rand: int = 1,
                 color_list=List[T_Exp,],
                 scale_list=List[T_Exp,],
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
    def name(self):
        return f"soy:seqt {self.x_list} {self.y_list} {self.z_list} {self.life} {self.rand} {self.color_list} {self.scale_list} '{self.texture}'"
