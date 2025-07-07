import socket
import json
from models.position import Position
from models.orientation import Orientation
from models.obstacle import Obstacle
from rover.rover import Rover

rover = Rover(10, 10, Position(0, 0, Orientation.N), [Obstacle(3, 3)])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("localhost", 9999))
    s.listen()
    print("Rover en attente de Mission Control...")

    while True:
        conn, _ = s.accept()
        with conn:
            print("Connecté.")
            data = conn.recv(1024)
            if not data:
                continue  # on passe à la prochaine connexion
            try:
                req = json.loads(data.decode())
                response = rover.execute_commands(req["commands"])
                conn.sendall(json.dumps(response).encode())
            except Exception as e:
                conn.sendall(json.dumps({"status": "ERROR", "message": str(e)}).encode())
