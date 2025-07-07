
from interfaces.icommand_listener import ICommandListener
from models.position import Position
from models.orientation import Orientation
from models.obstacle import Obstacle

class Rover(ICommandListener):
    def __init__(self, width, height, start: Position, obstacles: list[Obstacle]):
        self.width = width
        self.height = height
        self.position = start
        self.obstacles = {(o.x, o.y) for o in obstacles}
        self.stopped = False

    def execute_commands(self, commands: str) -> dict:
        ValidCommands = {'A', 'R', 'G', 'D'}
        commands = commands.strip().upper()
        for cmd in commands:
            if cmd not in ValidCommands:
                return {
                    "status": "ERROR",
                    "message": f"Commande invalide: {cmd}. Utilisez A (Avancer), R (Reculer), G (Gauche), D (Droite)",
                    "positions": self.position.__dict__,
                }
            if self.stopped:
                break
            match cmd:
                case 'A':
                    self.move(1)
                case 'R':
                    self.move(-1)
                case 'G':
                    self.turn_left()
                case 'D':
                    self.turn_right()
                case _:
                    raise ValueError(f"Commande inconnue: {cmd}")
        return {
            "status": "OBSTACLE" if self.stopped else "OK",
            "position": {
                "x": self.position.x,
                "y": self.position.y,
                "orientation": self.position.orientation.value
            }
        }

    def move(self, step):
        dx, dy = 0, 0
        match self.position.orientation:
            case Orientation.N:
                dy = step
            case Orientation.S:
                dy = -step
            case Orientation.E:
                dx = step
            case Orientation.W:
                dx = -step

        nx = (self.position.x + dx) % self.width
        ny = (self.position.y + dy) % self.height

        if (nx, ny) in self.obstacles:
            self.stopped = True
        else:
            self.position.x = nx
            self.position.y = ny

    def turn_left(self):
        dirs = [Orientation.N, Orientation.W, Orientation.S, Orientation.E]
        i = dirs.index(self.position.orientation)
        self.position.orientation = dirs[(i + 1) % 4]

    def turn_right(self):
        dirs = [Orientation.N, Orientation.E, Orientation.S, Orientation.W]
        i = dirs.index(self.position.orientation)
        self.position.orientation = dirs[(i + 1) % 4]
