import socket
import json
import random

from models.position import Position
from models.orientation import Orientation
from models.obstacle import Obstacle
from rover.rover import Rover

# === PARAMÈTRES ===
WIDTH, HEIGHT = 10, 10
START_POS = Position(0, 0, Orientation.N)

# === GÉNÉRATION ALÉATOIRE D'OBSTACLES ===
def generate_random_obstacles(width, height, start_x=0, start_y=0, min_obstacles=5, max_obstacles=15):
    num_obstacles = random.randint(min_obstacles, max_obstacles)
    obstacles = set()

    while len(obstacles) < num_obstacles:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        if (x, y) == (start_x, start_y):
            continue  # Ne pas bloquer le point de départ

        obstacles.add((x, y))

    return [Obstacle(x, y) for x, y in obstacles]

# Générer les obstacles au démarrage du serveur
obstacles = generate_random_obstacles(WIDTH, HEIGHT, start_x=START_POS.x, start_y=START_POS.y)

# Affichage pour debug (tu peux le supprimer après)
print("🪨 Obstacles générés :", [(o.x, o.y) for o in obstacles])

# === INITIALISATION DU ROVER ===
rover = Rover(WIDTH, HEIGHT, START_POS, obstacles)

# === SERVEUR SOCKET ===
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("localhost", 9999))
    s.listen()
    print("🛰️ Rover en attente de Mission Control...")

    while True:
        conn, _ = s.accept()
        with conn:
            print("📡 Connecté.")
            data = conn.recv(1024)
            if not data:
                continue
            try:
                req = json.loads(data.decode())
                response = rover.execute_commands(req["commands"])
                conn.sendall(json.dumps(response).encode())
            except Exception as e:
                conn.sendall(json.dumps({"status": "ERROR", "message": str(e)}).encode())