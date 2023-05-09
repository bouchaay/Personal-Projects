# Jeu de table de multiplication simple pour enfants

import random

# Fonction qui affiche le menu
def menu():
    print("Menu")
    print("1. Jouer")
    print("2. Quitter")

# Fonction qui affiche le jeu
def jeu():
    while True :
    # On choisit deux nombres aléatoires entre 1 et 10
        a = random.randint(1, 10)
        b = random.randint(1, 10)
    # On demande à l'utilisateur de calculer le produit
        print("Quel est le produit de", a, "et", b, "?")
    # On lit la réponse de l'utilisateur
        reponse = int(input())
    # On compare la réponse de l'utilisateur avec le produit
        if reponse == a * b:
            print("Bravo!")
        else:
            print("Dommage, le produit est", a * b)
            break

# Fonction principale
def main():
    # On affiche le menu
    menu()
    # On lit le choix de l'utilisateur
    choix = int(input())
    # On exécute le choix de l'utilisateur
    if choix == 1:
        jeu()
    elif choix == 2:
        print("Au revoir!")
    else:
        print("Choix invalide!")

# Appel de la fonction principale
main()
