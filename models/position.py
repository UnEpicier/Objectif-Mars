
from dataclasses import dataclass
from .orientation import Orientation

@dataclass
class Position:
    x: int
    y: int
    orientation: Orientation
