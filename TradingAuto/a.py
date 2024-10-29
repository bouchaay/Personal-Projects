import MetaTrader5 as mt5
import pandas as pd
import time
import meta_settings as ms

# Connexion à MetaTrader 5
ms.init_connect()

# Paramètres de l'instrument
symbol = "BTCUSD"
number_of_ticks = 1000
points_indent = 10

# Fonction pour récupérer les ticks et afficher les prix
def display_ticks():
    ticks = []  # Liste pour stocker les ticks

    while len(ticks) < number_of_ticks:
        last_tick = mt5.symbol_info_tick(symbol)
        if last_tick is None:
            print("Erreur lors de la récupération des ticks.")
            break
        
        # Ajout des valeurs bid et ask à la liste
        ticks.append((last_tick.bid, last_tick.ask))
        
        # Affichage des valeurs bid et ask
        print(f"Bid = {last_tick.bid}, Ask = {last_tick.ask}")

        time.sleep(1)  # Attendre 1 seconde avant d'obtenir le prochain tick

    # Convertir les ticks en DataFrame pour un éventuel traitement ultérieur
    df_ticks = pd.DataFrame(ticks, columns=['Bid', 'Ask'])
    print("\nDonnées de ticks :")
    print(df_ticks)

# Lancer la fonction d'affichage des ticks
display_ticks()

# Fermeture de la connexion à MetaTrader 5
mt5.shutdown()
