import socket
import json
from src.network.interfaces.inetwork_server import INetworkServer
from src.rover.models.position import Position
from src.rover.models.orientation import Orientation
from src.rover.models.obstacle import Obstacle
from src.rover.rover import Rover

class SocketServer(INetworkServer):
    def __init__(self, host: str = "localhost", port: int = 9999):
        self._host = host
        self._port = port
        self._rover = None

    def start(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self._host, self._port))
            s.listen()
            print("🛰️ Rover en attente de Mission Control...")

            while True:
                conn, _ = s.accept()
                with conn:
                    print("📡 Connecté.")
                    data = conn.recv(4096)
                    if not data:
                        continue

                    try:
                        req = json.loads(data.decode())

                        if req["type"] == "INIT":
                            width = req["map"]["width"]
                            height = req["map"]["height"]
                            start = req["map"]["start"]
                            obstacles_data = req["map"]["obstacles"]

                            start_pos = Position(start["x"], start["y"], Orientation[start["orientation"]])
                            obstacles = [Obstacle(o["x"], o["y"]) for o in obstacles_data]

                            self._rover = Rover(width, height, start_pos, obstacles)
                            conn.sendall(json.dumps({"status": "OK", "message": "Carte initialisée"}).encode())

                        elif req["type"] == "COMMANDS":
                            if self._rover is None:
                                raise Exception("Le rover n'a pas encore été initialisé.")
                            response = self._rover.execute_commands(req["commands"])
                            conn.sendall(json.dumps(response).encode())

                        else:
                            conn.sendall(json.dumps({"status": "ERROR", "message": "Type de requête inconnu"}).encode())

                    except Exception as e:
                        conn.sendall(json.dumps({"status": "ERROR", "message": str(e)}).encode())
