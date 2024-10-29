import MetaTrader5 as mt5
import pandas as pd
from tkinter import messagebox
import time
import numpy as np
from collections import deque
import threading
import meta_settings as ms
import bot_order_tracking as bot
from market import *
import os

if not os.path.exists("data"):
    os.makedirs("data")

# Connexion à MetaTrader 5
ms.init_connect()

# Paramètres de l'instrument
symbol = "XAUUSD"

# Paramètres de l'EMA
ema10_period = 10
ema20_period = 20
ema30_period = 30
ema60_period = 60
ema120_period = 120
ema180_period = 180
ema240_period = 240
ticks_queue = deque(maxlen=ema240_period)  # Garder une taille max pour le calcul de l'EMA 200

# Paramètres de la gestion de l'argent
pips = 3 # Pips pour le TP et SL
initial_lot = 0.05 # Taille initiale du lot
lot_multiplicator = 2 # Multiplicateur de lot en cas de perte

# Paramètres de la stratégie
ratio_tp = 1.2 # Ratio de profit (Profit = pips x ratio_tp)
ratio_sl = 1 # Ratio de perte (Perte = pips x ratio_sl)
nombre_position = 1 # Nombre de position à ouvrir

# Paramètres de la variation
variation_min = 2 # Variation minimale
variation_condition = False # Condition de variation

# Variables pour gérer les ordres
position_ouverte = False # Indique si une position est actuellement ouverte
current_lot_size = initial_lot # Taille actuelle du lot
ema10, ema20, ema30, ema60, ema120, ema180, ema240 = None, None, None, None, None, None, None # Valeurs actuelles des EMAs

# Variables pour le suivi des performances
total_trades = 0      # Nombre total de trades
winning_trades = 0    # Nombre de trades gagnants
losing_trades = 0     # Nombre de trades perdants
total_profit = 0.0    # Profit total en devise
max_consecutive_loss = 0 # Nombre maximum de pertes consécutives
consecutive_loss = 0 # Nombre de pertes consécutives actuelles

import os

# Fonction pour lire les statistiques existantes depuis le fichier
def read_stats_from_file():
    if not os.path.exists("data/trading_stats.txt"):
        # Valeurs par défaut si le fichier n'existe pas encore
        return 0, 0, 0, 0, 0

    with open("data/trading_stats.txt", "r") as file:
        line = file.readline().strip()
        
        # Vérifier que la ligne contient des données
        if not line:
            # Si le fichier est vide, retourner les valeurs par défaut
            return 0, 0, 0, 0, 0

        parts = line.split(", ")
        
        # Extraction des valeurs avec vérification de chaque partie
        try:
            total_trades = int(parts[0].split(": ")[1]) if len(parts) > 0 else 0
            winning_trades = int(parts[1].split(": ")[1]) if len(parts) > 1 else 0
            losing_trades = int(parts[2].split(": ")[1]) if len(parts) > 2 else 0
            max_consecutive_loss = int(parts[3].split(": ")[1]) if len(parts) > 3 else 0
            consecutive_loss = int(parts[4].split(": ")[1]) if len(parts) > 4 else 0
        except (ValueError, IndexError):
            # En cas d'erreur de format, utiliser les valeurs par défaut
            return 0, 0, 0, 0, 0

        return total_trades, winning_trades, losing_trades, max_consecutive_loss, consecutive_loss


# Fonction pour sauvegarder les statistiques mises à jour dans le fichier
def save_stats_to_file(total_trades, winning_trades, losing_trades, max_consecutive_loss, consecutive_loss):
    with open("data/trading_stats.txt", "w") as file:
        file.write(f"Total Trades: {total_trades}, Winning Trades: {winning_trades}, Losing Trades: {losing_trades}, Win Rate: {calculate_win_rate()}%, Max Consecutive Loss: {max_consecutive_loss}, Current Consecutive Losses: {consecutive_loss}\n")
    print("Statistiques sauvegardées dans le fichier.")

# Exemple d'utilisation avec mise à jour
def update_stats(result_type):
    # Lire les statistiques actuelles
    total_trades, winning_trades, losing_trades, max_consecutive_loss, consecutive_loss = read_stats_from_file()
    print(f"Avant mise à jour - Total Trades: {total_trades}, Winning Trades: {winning_trades}, Losing Trades: {losing_trades}, Max Consecutive Loss: {max_consecutive_loss}, Current Consecutive Losses: {consecutive_loss}")

    # Mettre à jour les statistiques
    total_trades += 1
    if result_type == "TP":
        winning_trades += 1
        consecutive_loss = 0
    elif result_type == "SL":
        losing_trades += 1
        consecutive_loss += 1
        max_consecutive_loss = max(max_consecutive_loss, consecutive_loss)

    # Sauvegarder les statistiques mises à jour dans le fichier
    save_stats_to_file(total_trades, winning_trades, losing_trades, max_consecutive_loss, consecutive_loss)
    print(f"Après mise à jour - Total Trades: {total_trades}, Winning Trades: {winning_trades}, Losing Trades: {losing_trades}, Max Consecutive Loss: {max_consecutive_loss}, Current Consecutive Losses: {consecutive_loss}")

# Calcul du taux de réussite
def calculate_win_rate():
    total_trades, winning_trades, _, _, _ = read_stats_from_file()
    if total_trades > 0:
        return (winning_trades / total_trades) * 100
    return 0

# Remplace la fonction update_profit_and_stats par update_stats

def update_stats_after_trade(result_type):
    # Appel de la fonction update_stats pour mettre à jour et enregistrer les statistiques
    update_stats(result_type)
    # Affichage des statistiques mises à jour
    total_trades, winning_trades, losing_trades, max_consecutive_loss, consecutive_loss = read_stats_from_file()
    print(f"Après sauvegarde - Total Trades: {total_trades}, Winning Trades: {winning_trades}, Losing Trades: {losing_trades}, Win Rate: {calculate_win_rate()}%, Max Consecutive Loss: {max_consecutive_loss}, Current Consecutive Losses: {consecutive_loss}")

# Fonction pour calculer l'EMA
def calculate_ema(data, period):
    return pd.Series(data).ewm(span=period, adjust=False).mean().iloc[-1]

# Fonction pour gérer les ticks dans un thread séparé
def manage_ticks():
    global ema10, ema20, ema30, ema60, ema120, ema180, ema240, variation_condition

    i = 0
    while True:
        last_tick = mt5.symbol_info_tick(symbol)
        if last_tick is None:
            print("Erreur lors de la récupération des ticks.")
        else:

            i += 1
            print(f"Tick {i} - Bid: {last_tick.bid}")
            # Ajouter le prix bid à la file pour le calcul des EMA
            ticks_queue.append(last_tick.bid)

            # Convertir la queue pour calculer les EMA
            if len(ticks_queue) >= ema240_period:  # S'assurer que nous avons suffisamment de données pour l'EMA 240
                ema10 = ticks_queue[-1]
                ema20 = (ticks_queue[-1] + ticks_queue[-2])/2
                ema30 = calculate_ema(list(ticks_queue), ema30_period)
                ema60 = calculate_ema(list(ticks_queue), ema60_period)
                ema120 = calculate_ema(list(ticks_queue), ema120_period)
                ema180 = calculate_ema(list(ticks_queue), ema180_period)
                ema240 = calculate_ema(list(ticks_queue), ema240_period)
                
                # Vérifier si la variation est atteinte
                min_ema240 = min(ticks_queue)
                max_ema240 = max(ticks_queue)
                variance_ema240 = abs(max_ema240 - min_ema240)
                if variance_ema240 >= variation_min:
                    variation_condition = True
                else :
                    variation_condition = False

            # Attendre 1 seconde avant de récupérer le prochain tick
            time.sleep(1)

# Fonction pour gérer les positions en fonction des EMA
def manage_trades():
    global position_ouverte, current_lot_size

    while True:
        if ema10 is not None and ema30 is not None and ema20 is not None and ema60 is not None and ema120 is not None and ema180 is not None and ema240 is not None:
            # Si aucune position n'est ouverte, en ouvrir une nouvelle en fonction des EMA
            if not position_ouverte:
                last_tick = mt5.symbol_info_tick(symbol)
                if last_tick is None:
                    print("Erreur lors de la récupération des ticks.")
                    break

                # Buy signal (EMA croissants et le dernier prix est supérieur à l'EMA 60)
                if ema30 > ema60 and ema60 > ema120 and ema120 > ema180 and ema180 > ema240 and last_tick.bid > ema30 and variation_condition:
                    print("Signal d'achat détecté.")
                    tp = last_tick.ask + (pips * ratio_tp)  # Objectif de profit
                    stop_loss = last_tick.ask - (pips*ratio_sl)  # Stop loss
                    trade_principal = 0
                    for i in range(nombre_position):
                        trade_principal += 1
                        result = open_buy_order(symbol, current_lot_size, tp, stop_loss)
                    

                        if result.retcode == mt5.TRADE_RETCODE_DONE:
                            #print("Ordre d'achat exécuté avec succès.")
                            position_ouverte = True
                            # Suivi de l'ordre (bot_order_tracking attend SL ou TP)
                            if trade_principal == 1:
                                order_thread = threading.Thread(target=track_order, args=(result.order,))
                                order_thread.daemon = True
                                order_thread.start()
                        else:
                            print(f"Erreur lors de l'ouverture de la position : {result.comment}")
                # Sell signal (EMA décroissants et le dernier prix est inférieur à l'EMA 60)
                elif ema30 < ema60 and ema60 < ema120 and ema120 < ema180 and ema180 < ema240 and last_tick.bid < ema30 and variation_condition:
                    print("Signal de vente détecté.")
                    tp = last_tick.bid - (pips * ratio_tp)  # Objectif de profit
                    stop_loss = last_tick.bid + (pips*ratio_sl)  # Stop loss
                    trade_principal = 0
                    for i in range(nombre_position):
                        trade_principal += 1
                        result = open_sell_order(symbol, current_lot_size, tp, stop_loss)
                        if result.retcode == mt5.TRADE_RETCODE_DONE:
                            #print("Ordre de vente exécuté avec succès.")
                            position_ouverte = True

                            # Suivi de l'ordre (bot_order_tracking attend SL ou TP)
                            if trade_principal == 1:
                                order_thread = threading.Thread(target=track_order, args=(result.order,))
                                order_thread.daemon = True
                                order_thread.start()
                        else:
                            print(f"Erreur lors de l'ouverture de la position : {result.comment}")
                 
        time.sleep(1)

# Fonction pour gérer le suivi et le résultat de l'ordre (TP ou SL)
def track_order(order_id):
    global position_ouverte, current_lot_size, lot_multiplied

    print(f"Suivi de l'ordre {order_id} en cours...")
    order_result = bot.bot_order_tracking2(order_id)

    # Gérer le résultat de l'ordre
    if order_result == "TP":
        current_lot_size = initial_lot
        update_stats_after_trade("TP")
        print("TP -> LOT initial : ", current_lot_size)
    elif order_result == "SL":
        current_lot_size *= lot_multiplicator
        update_stats_after_trade("SL")
        print("SL -> LOT x", lot_multiplicator, ": ", current_lot_size)
    else:
        print("Erreur ou position non trouvée.")

    # Une fois que l'ordre est terminé (TP ou SL), permettre l'ouverture d'une nouvelle position
    position_ouverte = False



# Lancer la gestion des ticks et des trades dans des threads séparés
# Lancer la gestion des ticks et des trades dans des threads séparés
ticks_thread = threading.Thread(target=manage_ticks)
ticks_thread.start()

trade_thread = threading.Thread(target=manage_trades)
trade_thread.start()

# Attendre que les threads se terminent
ticks_thread.join()
trade_thread.join()

# Fermeture de la connexion à MetaTrader 5 à la fin (si nécessaire)
# mt5.shutdown()
