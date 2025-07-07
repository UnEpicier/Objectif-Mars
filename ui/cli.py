from mission_control.mission_control import MissionControl

# Lettres autorisées
COMMANDES_VALIDES = {'A', 'R', 'G', 'D'}

if __name__ == "__main__":
    mc = MissionControl()
    while True:
        cmds = input("Commandes pour le Rover (A, R, G, D) : ").strip().upper()
        if cmds == "QUIT":
            break

        # Vérification des lettres invalides
        if not all(c in COMMANDES_VALIDES for c in cmds):
            print("⚠️  Commande invalide. Utilisez uniquement les lettres : A (Avancer), R (Reculer), G (Gauche), D (Droite)")
            continue

        # Envoi des commandes valides
        result = mc.send_commands(cmds)
        print(">> Résultat:", result)
