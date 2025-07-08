from typing import NamedTuple, Optional

class MoveResult(NamedTuple):
    success: bool
    obstacle_position: Optional[tuple[int, int]]
