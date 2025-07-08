from src.mission_control.icommand_sender import ICommandSender

COMMANDES_VALIDES = {'A', 'R', 'G', 'D'}
WIDTH, HEIGHT = 10, 10
orientation_symbols = { "N": "↑", "S": "↓", "E": "→", "W": "←" }

obstacles_detected = set()

def afficher_carte(pos):
    grid = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for ox, oy in obstacles_detected:
        grid[oy][ox] = "O"

    x, y = pos["x"], pos["y"]
    orientation = pos["orientation"]
    grid[y][x] = f"R{orientation_symbols.get(orientation, '?')}"
    print("\n📍 Carte du terrain :")
    for row in reversed(grid):
        print(" ".join(row))
    print()

def run_cli(command_sender: ICommandSender):
    try:
        print("🛰️ Initialisation de la carte...")
        init_response = command_sender.send_init()
        if init_response["status"] != "OK":
            print("❌ Échec de l'initialisation :", init_response["message"])
            exit(1)

        print("✅ Carte initialisée avec succès.")
        result = command_sender.send_commands("")
        if result["status"] == "OK":
            afficher_carte(result["position"])

        while True:
            cmds = input("Commandes pour le Rover (A, R, G, D) : ").strip().upper()
            if cmds == "QUIT":
                break

            if not all(c in COMMANDES_VALIDES for c in cmds):
                print("⚠️  Commande invalide. Utilisez uniquement les lettres : A (Avancer), R (Reculer), G (Gauche), D (Droite)")
                continue

            result = command_sender.send_commands(cmds)

            if result["status"] == "OBSTACLE":
                pos = result["position"]
                obs = result.get("obstacle")
                if obs:
                    print(f"🚧 Obstacle détecté à ({obs['x']}, {obs['y']})")
                    obstacles_detected.add((obs["x"], obs["y"]))

            elif result["status"] == "ERROR":
                print("❌ Erreur :", result["message"])

            afficher_carte(result["position"])
    finally:
        command_sender.send_commands("QUIT")
        print("Connexion terminée")
