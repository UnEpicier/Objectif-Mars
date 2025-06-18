class MissionControl:
    # 1. Setup vars
    # 2. Print state in console (loop of clear / print / clear / print)
    def __init__(self, network):
        self.__network = network
        self.__lastKnownPos: tuple[int, int] = (0,0)
        self.__mapSize: int = 50
        # Store discovered places (obstacle or empty)
        self.__mapData = None

    # Send command to rover, receive new rover coords and 
    # if it has encountered an obstacle
    def sendCommandToRover(self, commands: str) -> str:
        return ""

    # Take last known rover position, map size and map data and print 2D string rendered map (ascii art)
    def getMap(self) -> str:
        return ""

    def start(self):
        while(True):
            print(self.getMap())