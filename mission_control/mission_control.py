
from interfaces.icommand_sender import ICommandSender
import socket
import json

class MissionControl(ICommandSender):
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port

    def send_commands(self, commands: str) -> dict:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(json.dumps({"commands": commands}).encode())
            response = s.recv(1024)
            return json.loads(response.decode())
    
    def close(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.close()
