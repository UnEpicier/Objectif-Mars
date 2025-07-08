
from abc import ABC, abstractmethod

class ICommandSender(ABC):
    @abstractmethod
    def send_commands(self, commands: str) -> dict:
        pass
