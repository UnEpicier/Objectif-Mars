from __future__ import annotations

from src.rover.icommand_listener import ICommandListener
from src.rover.models.position import Position
from src.rover.models.orientation import Orientation
from src.rover.models.obstacle import Obstacle

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
        self.stopped = False
        detected_obstacle = None

        for cmd in commands:
            if cmd not in ValidCommands:
                return {
                    "status": "ERROR",
                    "message": f"Commande invalide: {cmd}. Utilisez A (Avancer), R (Reculer), G (Gauche), D (Droite)",
                    "positions": self.position.__dict__,
                }

            if cmd in {'A', 'R'}:
                step = 1 if cmd == 'A' else -1
                moved, obstacle_pos = self.move(step)
                if not moved:
                    self.stopped = True
                    detected_obstacle = obstacle_pos
                    break
            elif cmd == 'G':
                self.turn_left()
            elif cmd == 'D':
                self.turn_right()

        response = {
            "status": "OBSTACLE" if self.stopped else "OK",
            "position": {
                "x": self.position.x,
                "y": self.position.y,
                "orientation": self.position.orientation.value
            }
        }

        if detected_obstacle:
            response["obstacle"] = {"x": detected_obstacle[0], "y": detected_obstacle[1]}

        return response

    def move(self, step) -> tuple[bool, tuple[int, int] | None]:
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
            return False, (nx, ny)
        else:
            self.position.x = nx
            self.position.y = ny
            return True, None

    def turn_left(self):
        dirs = [Orientation.N, Orientation.W, Orientation.S, Orientation.E]
        i = dirs.index(self.position.orientation)
        self.position.orientation = dirs[(i + 1) % 4]

    def turn_right(self):
        dirs = [Orientation.N, Orientation.E, Orientation.S, Orientation.W]
        i = dirs.index(self.position.orientation)
        self.position.orientation = dirs[(i + 1) % 4]