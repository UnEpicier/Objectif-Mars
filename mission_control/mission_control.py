from interfaces.icommand_sender import ICommandSender
import socket
import json
import random

class MissionControl(ICommandSender):
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.map_width = 10
        self.map_height = 10

    def generate_map(self):
        start = {"x": 0, "y": 0, "orientation": "N"}

        num_obstacles = random.randint(5, 10)
        obstacles = []

        while len(obstacles) < num_obstacles:
            x = random.randint(0, self.map_width - 1)
            y = random.randint(0, self.map_height - 1)

            if (x, y) != (0, 0) and {"x": x, "y": y} not in obstacles:
                obstacles.append({"x": x, "y": y})

        return {
            "width": self.map_width,
            "height": self.map_height,
            "start": start,
            "obstacles": obstacles
        }

    def send_init(self):
        carte = self.generate_map()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(json.dumps({"type": "INIT", "map": carte}).encode())
            response = s.recv(4096)
            return json.loads(response.decode())

    def send_commands(self, commands: str) -> dict:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(json.dumps({"type": "COMMANDS", "commands": commands}).encode())
            response = s.recv(4096)
            return json.loads(response.decode())
