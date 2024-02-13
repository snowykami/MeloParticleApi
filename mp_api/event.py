from .particle import BaseParticle
from .mp_typing import *


class BaseEvent(object):
    def __init__(self,
                 time: int = 0
                 ):
        self.time = time

    def __str__(self):
        return "<BaseEvent>"

    @property
    def command(self):
        return "say BaseEvent"


class ExecuteEvent(BaseEvent):
    def __init__(self,
                 sub_commands: List[str],
                 run_event: BaseEvent,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.sub_commands = sub_commands
        self.run_event = run_event

    @property
    def command(self):
        return f"execute {' '.join(self.sub_commands)} run {self.run_event.command}"


class FunctionEvent(BaseEvent):
    def __init__(self,
                 function: 'MCFunction',
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.function = function

    @property
    def command(self):
        return f"function {self.function.namespace}:{self.function.name}"


class ParticleEvent(BaseEvent):
    def __init__(self,
                 particle: BaseParticle,
                 pos: T_Pos = ('~', '~', '~'),
                 delta: T_Vec3 = (0, 0, 0),
                 speed: T_Num = 0,
                 count: int = 1,
                 force: str = 'force',
                 # force | normal
                 player: str = '@a',
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.particle = particle
        self.pos = pos
        self.delta = delta
        self.speed = speed
        self.count = count
        self.force = force
        self.player = player

    def __str__(self):
        return "<ParticleEvent>"

    @property
    def command(self):
        return f"particle {self.particle.name} {self.pos[0]} {self.pos[1]} {self.pos[2]} {self.delta[0]} {self.delta[1]} {self.delta[2]} {self.speed} {self.count} {self.force} {self.player}"


class ScheduleEvent(BaseEvent):
    def __init__(self,
                 function: 'MCFunction',
                 time: int,
                 unit: str = 't',
                 # append | replace
                 append: str = ''
                 ):
        super().__init__()
        self.function = function
        self.time = time
        self.unit = unit
        self.append = append

    @property
    def command(self):
        return f"schedule function {self.function.namespace}:{self.function.name} {self.time}{self.unit} {self.append}"


class MCFunction(object):
    def __init__(self,
                 name: str,
                 commands: List[str] = None,
                 namespace: str = None,
                 ):
        self.name = name
        self.namespace = namespace
        if commands is None:
            self.commands = []

    def add_command(self, command: str):
        self.commands.append(command)

    def add_event(self, event: BaseEvent):
        self.commands.append(event.command)

    def __str__(self):
        return f"<MCFunction {self.name}>"

    def __repr__(self):
        return f"<MCFunction {self.name}>"