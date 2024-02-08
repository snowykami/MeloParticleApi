from .mp_typing import *
from .draw import Color


class Particle(object):
    def __init__(
            self,
            name: str,
            pos: T_Pos = ("~", "~", "~"),
            delta: T_Vec3 = (0, 0, 0),
            speed: T_Num = 0,
            count: int = 1,
            force: str = "force",
            viewer: str = "@a",
    ):
        self._name = name
        self.pos = pos
        self.delta = delta
        self.speed = speed
        self.count = count
        self.force = force
        self.viewer = viewer

    @property
    def command(self) -> str:
        return f"particle {self.name} {self.pos[0]} {self.pos[1]} {self.pos[2]} {self.delta[0]} {self.delta[1]} {self.delta[2]} {self.speed} {self.count} {self.force} {self.viewer}"

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


# 一级粒子类
class BestParticle(Particle):
    def __init__(
            self,
            x_exp: str = '0',
            y_exp: str = '0',
            z_exp: str = '0',
            life: int = '0',
            rand: int = '1',
            color_exp: str = str(Color('FFFFFF').get_int()),
            **kwargs,
    ):
        # 为 SoyBest 实例设置一个默认的 name
        super().__init__(name='soy:best', **kwargs)
        self.x_exp = x_exp
        self.y_exp = y_exp
        self.z_exp = z_exp
        self.life = life
        self.rand = rand
        self.color_exp = color_exp

    @property
    def name(self) -> str:
        return f"soy:best '{self.x_exp}' '{self.y_exp}' '{self.z_exp}' {self.life} {self.rand} '{self.color_exp}'"


class ColorParticle(Particle):
    def __init__(
            self,
            color: Color | T_Color = Color('FFFFFF'),
            **kwargs,
    ):
        super().__init__(name='soy:color_particle', **kwargs)
        self.color = Color(color)

    @property
    def name(self) -> str:
        return f"soy:color_particle {self.color.get_int()}"


class SeqParticle(Particle):
    def __init__(
            self,
            xList=None,
            yList=None,
            zList=None,
            life: int = 1,
            rand: int = 1,
            colorList: List[Color | T_Color,] = None,
            scaleList: List[T_Num] = None,
            **kwargs,
    ):
        kwargs['name'] = 'soy:seq'
        super().__init__(**kwargs)

        if xList is None:
            xList = [0, ]
        if zList is None:
            zList = [0, ]
        if yList is None:
            yList = [0, ]

        if scaleList is None:
            scaleList = [1, ]
        if colorList is None:
            colorList = [Color('FFFFFF'), ]

        self.x_list = xList
        self.y_list = yList
        self.z_list = zList
        self.life = life
        self.rand = rand
        self.color_list = colorList
        self.scale_list = scaleList

    @property
    def name(self) -> str:
        return f"{self._name} {self.x_list} {self.y_list} {self.z_list} {self.life} {self.rand} {[color.get_int() for color in self.color_list]} {self.scale_list}"


class LifeParticle(Particle):
    """该粒子并未实现"""

    def __init__(
            self,
            life: int = 1,
            rand: int = 1,
            **kwargs,
    ):
        super().__init__(name='soy:life_particle', **kwargs)
        self.life = life
        self.rand = rand

    @property
    def name(self) -> str:
        return f"{self._name} {self.life} {self.rand}"


class LifeColorParticle(ColorParticle):
    def __init__(
            self,
            life: int = 1,
            rand: int = 1,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.life = life
        self.rand = rand

    @property
    def name(self) -> str:
        return f"soy:life_color_particle {self.color.get_int()} {self.life} {self.rand}"


class LifeColorTextureParticle(LifeColorParticle):
    def __init__(self, texture: str, **kwargs):
        super().__init__(**kwargs)
        self.texture = texture

    @property
    def name(self) -> str:
        return f"soy:life_color_texture {self.color.get_int()} {self.life} {self.rand} '{self.texture}'"


class LifeEndRodParticle(LifeParticle):
    def __init__(self, **kwargs):
        kwargs['name'] = 'soy:life_end_rod'
        super().__init__(**kwargs)


class LifeFireworkParticle(LifeParticle):
    def __init__(self, **kwargs):
        kwargs['name'] = 'soy:life_firework'
        super().__init__(**kwargs)


class SeqtParticle(SeqParticle):
    def __init__(self, texture: str, **kwargs):
        kwargs['name'] = 'soy:seqt'
        super().__init__(**kwargs)
        self.texture = texture

    @property
    def name(self) -> str:
        return super().name + f" '{self.texture}'"
