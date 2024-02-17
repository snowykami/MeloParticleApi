from typing import List, Union

from .particle import BaseParticle
from .mp_typing import T_Pos, T_Vec3, T_Num


class BaseEvent(object):
    def __init__(self, time: int = 0):
        """Initialize a BaseEvent.

        Args:
            time (int, optional): The time associated with the event. Defaults to 0.
        """
        self.time = time

    def __str__(self) -> str:
        """Return a string representation of the BaseEvent."""
        return "<BaseEvent>"

    @property
    def command(self) -> str:
        """Get the command associated with the BaseEvent.

        Returns:
            str: The command string.
        """
        return "say BaseEvent"


class ExecuteEvent(BaseEvent):
    def __init__(self, sub_commands: List[str], run_event: BaseEvent, **kwargs):
        """Initialize an ExecuteEvent.

        Args:
            sub_commands (List[str]): List of sub-commands for execution.
            run_event (BaseEvent): The event to run.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.sub_commands = sub_commands
        self.run_event = run_event

    @property
    def command(self) -> str:
        """Get the command associated with the ExecuteEvent.

        Returns:
            str: The command string.
        """
        return f"execute {' '.join(self.sub_commands)} run {self.run_event.command}"


class FillEvent(BaseEvent):
    def __init__(self, start: T_Pos, end: T_Pos, block: str, mode: str = 'replace', **kwargs):
        """Initialize a FillEvent.

        Args:
            start (T_Pos): Starting position.
            end (T_Pos): Ending position.
            block (str): The block to fill.
            mode (str, optional): Fill mode ('replace' by default).
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.start = start
        self.end = end
        self.block = block if ':' in block else f"minecraft:{block}"
        self.mode = mode

    @property
    def command(self) -> str:
        """Get the command associated with the FillEvent.

        Returns:
            str: The command string.
        """
        return f"fill {int(self.start[0])} {int(self.start[1])} {int(self.start[2])} " \
               f"{int(self.end[0])} {int(self.end[1])} {int(self.end[2])} {self.block} {self.mode}"


class FunctionEvent(BaseEvent):
    def __init__(self, function: 'MCFunction', **kwargs):
        """Initialize a FunctionEvent.

        Args:
            function (MCFunction): The function to call.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.function = function

    @property
    def command(self) -> str:
        """Get the command associated with the FunctionEvent.

        Returns:
            str: The command string.
        """
        return f"function {self.function.namespace}:{self.function.name}"


class ParticleEvent(BaseEvent):
    def __init__(self, particle: BaseParticle, pos: T_Pos = ('~', '~', '~'), delta: T_Vec3 = (0, 0, 0),
                 speed: T_Num = 0, count: int = 1, force: str = 'force', player: str = '@a', **kwargs):
        """Initialize a ParticleEvent.

        Args:
            particle (BaseParticle): The particle to spawn.
            pos (T_Pos, optional): Position to spawn the particle ('~' by default).
            delta (T_Vec3, optional): Velocity of the particle (default is no velocity).
            speed (T_Num, optional): Speed of the particle (0 by default).
            count (int, optional): Number of particles to spawn (1 by default).
            force (str, optional): Force mode ('force' by default).
            player (str, optional): Target player ('@a' by default).
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.particle = particle
        self.pos = pos
        self.delta = delta
        self.speed = speed
        self.count = count
        self.force = force
        self.player = player
        # Limit decimal places for pos and delta
        self.pos = tuple([f'{p:.5f}' if isinstance(p, float) else p for p in self.pos])
        self.delta = tuple([f'{p:.5f}' if isinstance(p, float) else p for p in self.delta])

    def __str__(self) -> str:
        """Return a string representation of the ParticleEvent."""
        return "<ParticleEvent>"

    @property
    def command(self) -> str:
        """Get the command associated with the ParticleEvent.

        Returns:
            str: The command string.
        """
        return f"particle {self.particle.name} {self.pos[0]} {self.pos[1]} {self.pos[2]} " \
               f"{self.delta[0]} {self.delta[1]} {self.delta[2]} {self.speed} {self.count} " \
               f"{self.force} {self.player}"


class ScheduleEvent(BaseEvent):
    def __init__(self, function: Union['MCFunction', str], time: int, unit: str = 't',
                 clear: bool = False, append: str = ''):
        """Initialize a ScheduleEvent.

        Args:
            function (Union['MCFunction', str]): The function to schedule.
            time (int): The time at which to schedule the function.
            unit (str, optional): The unit of time 't' by default.
            clear (bool, optional): Whether to clear the schedule ('False' by default).
            append (str, optional): Additional scheduling options ('' by default).
        """
        super().__init__()
        self.function = function
        self.time = time
        self.unit = unit
        self.append = append
        self.clear = clear

    @property
    def command(self) -> str:
        """Get the command associated with the ScheduleEvent.

        Returns:
            str: The command string.
        """
        function_name = f"{self.function.namespace}:{self.function.name}" if isinstance(self.function, MCFunction) else self.function
        if ':' not in function_name:
            function_name = f"minecraft:{function_name}"
        if self.clear:
            return f"schedule clear {function_name}"
        else:
            return f"schedule function {function_name} {self.time}{self.unit} {self.append}"


class SetBlockEvent(BaseEvent):
    def __init__(self, pos: T_Pos = ('~', '~', '~'), block: str = 'minecraft:air', mode: str = 'replace', **kwargs):
        """Initialize a SetBlockEvent.

        Args:
            pos (T_Pos, optional): The position to set the block ('~' by default).
            block (str, optional): The block to set ('minecraft:air' by default).
            mode (str, optional): Set block mode ('replace' by default).
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.pos = pos
        self.block = block if ':' in block else f"minecraft:{block}"
        self.mode = mode

    @property
    def command(self) -> str:
        """Get the command associated with the SetBlockEvent.

        Returns:
            str: The command string.
        """
        return f"setblock {int(self.pos[0])} {int(self.pos[1])} {int(self.pos[2])} {self.block} {self.mode}"


class MCFunction(object):
    def __init__(self, name: str, commands: List[str] = None, namespace: str = None):
        """Initialize an MCFunction.

        Args:
            name (str): The name of the function.
            commands (List[str], optional): List of commands within the function (None by default).
            namespace (str, optional): The namespace of the function (None by default).
        """
        self.name = name
        self.namespace = namespace
        if commands is None:
            self.commands = []

    def add_command(self, command: str):
        """Add a command to the MCFunction.

        Args:
            command (str): The command to add.
        """
        self.commands.append(command)

    def add_events(self, *events: BaseEvent):
        """Add a list of events to the MCFunction.

        Args:
            *events (BaseEvent): Variable number of events to add.
        """
        self.commands.extend([e.command for e in events])

    def __str__(self) -> str:
        """Return a string representation of the MCFunction."""
        return f"<MCFunction {self.name}>"

    def __repr__(self) -> str:
        """Return a string representation of the MCFunction for debugging purposes."""
        return f"<MCFunction {self.name}>"
