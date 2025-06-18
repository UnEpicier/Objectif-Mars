from enum import Enum
from Network import Network

class Ordre(Enum):
    AVANCER = "A"
    RECULER = "R"
    GAUCHE = "G"
    DROITE = "D"

class Rover:
    def __init__(self, network: Network) -> void:
        self.__network = network

    def Move(self, direction: Ordre):
        return "To do"

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z