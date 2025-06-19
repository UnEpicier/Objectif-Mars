
from abc import ABC, abstractmethod

class ICommandListener(ABC):
    @abstractmethod
    def execute_commands(self, commands: str) -> dict:
        pass
