from src.network.socket_server import SocketServer
from src.network.interfaces.inetwork_server import INetworkServer

def main():
    server: INetworkServer = SocketServer()
    server.start()

if __name__ == "__main__":
    main()
