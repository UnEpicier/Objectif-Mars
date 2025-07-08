from __future__ import annotations

from src.rover.icommand_listener import ICommandListener
from src.rover.models.move_result import MoveResult
from src.rover.models.position import Position
from src.rover.models.orientation import Orientation
from src.rover.models.obstacle import Obstacle

class Rover(ICommandListener):
    def __init__(self, width, height, start: Position, obstacles: list[Obstacle]):
        self._width = width
        self._height = height
        self._position = start
        self._obstacles = {(o.x, o.y) for o in obstacles}
        self._stopped = False

    def execute_commands(self, commands: str) -> dict:
        valid_commands = {'A', 'R', 'G', 'D'}
        commands = commands.strip().upper()
        self._stopped = False
        detected_obstacle = None

        for cmd in commands:
            if cmd not in valid_commands:
                return {
                    "status": "ERROR",
                    "message": f"Commande invalide: {cmd}. Utilisez A (Avancer), R (Reculer), G (Gauche), D (Droite)",
                    "positions": self._position.__dict__,
                }

            if cmd in {'A', 'R'}:
                step = 1 if cmd == 'A' else -1
                result = self._move(step)
                if not result.success:
                    self._stopped = True
                    detected_obstacle = result.obstacle_position
                    break
            elif cmd == 'G':
                self._turn_left()
            elif cmd == 'D':
                self._turn_right()

        response = {
            "status": "OBSTACLE" if self._stopped else "OK",
            "position": {
                "x": self._position.x,
                "y": self._position.y,
                "orientation": self._position.orientation.value
            }
        }

        if detected_obstacle:
            response["obstacle"] = {"x": detected_obstacle[0], "y": detected_obstacle[1]}

        return response

    def _move(self, step) -> MoveResult:
        dx, dy = 0, 0
        match self._position.orientation:
            case Orientation.N:
                dy = step
            case Orientation.S:
                dy = -step
            case Orientation.E:
                dx = step
            case Orientation.W:
                dx = -step

        nx = (self._position.x + dx) % self._width
        ny = (self._position.y + dy) % self._height

        if (nx, ny) in self._obstacles:
            return MoveResult(False, (nx, ny))
        else:
            self._position.x = nx
            self._position.y = ny
            return MoveResult(True, None)

    def _turn_left(self):
        dirs = [Orientation.N, Orientation.W, Orientation.S, Orientation.E]
        i = dirs.index(self._position.orientation)
        self._position.orientation = dirs[(i + 1) % 4]

    def _turn_right(self):
        dirs = [Orientation.N, Orientation.E, Orientation.S, Orientation.W]
        i = dirs.index(self._position.orientation)
        self._position.orientation = dirs[(i + 1) % 4]
