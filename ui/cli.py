from mission_control.mission_control import MissionControl

# Lettres autorisées
COMMANDES_VALIDES = {'A', 'R', 'G', 'D'}

# Taille de la grille (doit correspondre à celle du serveur)
WIDTH, HEIGHT = 10, 10

# Liste des obstacles découverts
obstacles_detected = set()

# Mapping pour afficher l'orientation du rover
orientation_symbols = {
    "N": "↑",
    "S": "↓",
    "E": "→",
    "W": "←"
}

def afficher_carte(pos):
    grid = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # Marquer les obstacles connus
    for ox, oy in obstacles_detected:
        grid[oy][ox] = "O"

    # Placer le rover
    x, y = pos["x"], pos["y"]
    orientation = pos["orientation"]
    grid[y][x] = f"R{orientation_symbols.get(orientation, '?')}"

    print("\n📍 Carte du terrain :")
    for row in reversed(grid):
        print(" ".join(row))
    print()

if __name__ == "__main__":
    mc = None
    try:
        mc = MissionControl()

        print("🛰️ Initialisation de la carte...")
        init_response = mc.send_init()
        if init_response["status"] != "OK":
            print("❌ Échec de l'initialisation :", init_response["message"])
            exit(1)

        print("✅ Carte initialisée avec succès.")
        result = mc.send_commands("") 
        if result["status"] == "OK":
            afficher_carte(result["position"])

        while True:
            cmds = input("Commandes pour le Rover (A, R, G, D) : ").strip().upper()
            if cmds == "QUIT":
                break

            if not all(c in COMMANDES_VALIDES for c in cmds):
                print("⚠️  Commande invalide. Utilisez uniquement les lettres : A (Avancer), R (Reculer), G (Gauche), D (Droite)")
                continue

            result = mc.send_commands(cmds)

            if result["status"] == "OBSTACLE":
                pos = result["position"]
                obs = result.get("obstacle")
                if obs:
                    print("🚧 Obstacle détecté à ({}, {})".format(obs["x"], obs["y"]))
                    obstacles_detected.add((obs["x"], obs["y"]))

            elif result["status"] == "ERROR":
                print("❌ Erreur :", result["message"])

            afficher_carte(result["position"])
    finally:
        if mc:
            mc.send_commands("QUIT")
            print("Connexion terminée")
