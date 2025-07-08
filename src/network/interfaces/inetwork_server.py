from abc import ABC, abstractmethod

class INetworkServer(ABC):
    @abstractmethod
    def start(self) -> None:
        pass
