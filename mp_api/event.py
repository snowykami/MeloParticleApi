from typing import Union

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


class FillEvent(BaseEvent):
    def __init__(self,
                 start: T_Pos,
                 end: T_Pos,
                 block: str,
                 mode: str = 'replace',
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.start = start
        self.end = end
        self.block = block
        if ':' not in block:
            self.block = f"minecraft:{block}"
        self.mode = mode

    @property
    def command(self):
        # int
        return f"fill {int(self.start[0])} {int(self.start[1])} {int(self.start[2])} {int(self.end[0])} {int(self.end[1])} {int(self.end[2])} {self.block} {self.mode}"


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
        # 限制pos, delta小数位
        self.pos = tuple([f'{p:.5f}' if isinstance(p, float) else p for p in self.pos])
        self.delta = tuple([f'{p:.5f}' if isinstance(p, float) else p for p in self.delta])

    def __str__(self):
        return "<ParticleEvent>"

    @property
    def command(self):
        return f"particle {self.particle.name} {self.pos[0]} {self.pos[1]} {self.pos[2]} {self.delta[0]} {self.delta[1]} {self.delta[2]} {self.speed} {self.count} {self.force} {self.player}"


class ScheduleEvent(BaseEvent):
    def __init__(self,
                 function: Union['MCFunction', str],
                 time: int,
                 unit: str = 't',
                 clear: bool = False,
                 # append | replace
                 append: str = ''
                 ):
        super().__init__()
        self.function = function
        self.time = time
        self.unit = unit
        self.append = append
        self.clear = clear

    @property
    def command(self):
        if isinstance(self.function, MCFunction):
            function_name = f"{self.function.namespace}:{self.function.name}"
        else:
            function_name = self.function
            if ':' not in function_name:
                function_name = f"minecraft:{function_name}"
        if self.clear:
            return f"schedule clear {function_name}"
        else:
            return f"schedule function {function_name} {self.time}{self.unit} {self.append}"


class SetBlockEvent(BaseEvent):
    def __init__(
            self,
            pos: T_Pos = ('~', '~', '~'),
            block: str = 'minecraft:air',
            mode: str = 'replace',
            # destroy | keep | replace
            **kwargs
    ):
        super().__init__(**kwargs)
        self.pos = pos
        self.block = block
        if ':' not in block:
            self.block = f"minecraft:{block}"
        self.mode = mode

    @property
    def command(self):
        return f"setblock {int(self.pos[0])} {int(self.pos[1])} {int(self.pos[2])} {self.block} {self.mode}"


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

    def add_command(self,
                    command: str
                    ):
        self.commands.append(command)

    def add_events(self,
                   *events: BaseEvent
                   ):
        self.commands.extend([e.command for e in events])

    def __str__(self):
        return f"<MCFunction {self.name}>"

    def __repr__(self):
        return f"<MCFunction {self.name}>"
