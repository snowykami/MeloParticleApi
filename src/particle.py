from mp_typing import *


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


class SoyBest(Particle):
    def __init__(
            self,
            x_exp: str,
            y_exp: str,
            z_exp: str,
            life: int,
            rand: int,
            color_exp: str,
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
