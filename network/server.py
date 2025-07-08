import socket
import json
from models.position import Position
from models.orientation import Orientation
from models.obstacle import Obstacle
from rover.rover import Rover

rover = None

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("localhost", 9999))
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
                    # Initialisation de la carte et du rover
                    width = req["map"]["width"]
                    height = req["map"]["height"]
                    start = req["map"]["start"]
                    obstacles_data = req["map"]["obstacles"]

                    start_pos = Position(start["x"], start["y"], Orientation[start["orientation"]])
                    obstacles = [Obstacle(o["x"], o["y"]) for o in obstacles_data]

                    rover = Rover(width, height, start_pos, obstacles)
                    conn.sendall(json.dumps({"status": "OK", "message": "Carte initialisée"}).encode())

                elif req["type"] == "COMMANDS":
                    if rover is None:
                        raise Exception("Le rover n'a pas encore été initialisé.")
                    response = rover.execute_commands(req["commands"])
                    conn.sendall(json.dumps(response).encode())

                else:
                    conn.sendall(json.dumps({"status": "ERROR", "message": "Type de requête inconnu"}).encode())

            except Exception as e:
                conn.sendall(json.dumps({"status": "ERROR", "message": str(e)}).encode())
