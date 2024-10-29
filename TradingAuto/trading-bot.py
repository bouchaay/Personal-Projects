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

# Connexion à MetaTrader 5
ms.init_connect()

threads = []

# Liste des symboles avec leurs paramètres spécifiques
symbols_params = {
    #"US30m": {"ema_periods": [6, 12, 18, 24], "initial_lot": 1, "pips": 20, "ratio": 1.2},
    "XAUUSD": {"ema_periods": [6, 12, 18, 24], "initial_lot": 0.5, "pips": 0.2, "ratio": 1},
    #"XAGUSD": {"ema_periods": [6, 12, 18, 24], "initial_lot": 0.2, "pips": 0.02, "ratio": 1},
    #"US500": {"ema_periods": [6, 12, 18, 24], "initial_lot": 0.95, "pips": 10, "ratio": 1},
    #"USTEC": {"ema_periods": [6, 12, 18, 24], "initial_lot": 0.95, "pips": 10, "ratio": 1},
    ##"EURUSD": {"ema_periods": [6, 12, 18, 24], "initial_lot": 0.95, "pips": 0.0002, "ratio": 1},
    #"GBPUSD": {"ema_periods": [6, 12, 18, 24], "initial_lot": 0.95, "pips": 0.0002, "ratio": 1},
    #"ETHUSD": {"ema_periods": [6, 12, 18, 24], "initial_lot": 0.95, "pips": 10, "ratio": 1},
    #"BTCUSD": {"ema_periods": [6, 12, 18, 24], "initial_lot": 0.2, "pips": 100, "ratio": 1}
}

# Variables pour gérer les ordres par symbole
positions_ouvertes = {symbol: False for symbol in symbols_params.keys()}  # Une position par symbole
lot_sizes = {symbol: params["initial_lot"] for symbol, params in symbols_params.items()}
ema_values = {symbol: [None] * len(params["ema_periods"]) for symbol, params in symbols_params.items()}

# Variables pour le suivi des performances globales
total_trades = 0      # Nombre total de trades
winning_trades = 0    # Nombre de trades gagnants
losing_trades = 0     # Nombre de trades perdants
total_profit = 0.0    # Profit total en devise

def calculate_win_rate():
    if total_trades > 0:
        return (winning_trades / total_trades) * 100
    return 0

def update_profit_and_stats(result_type):
    global total_trades, winning_trades, losing_trades
    
    total_trades += 1
    
    if result_type == "TP":
        winning_trades += 1
    elif result_type == "SL":
        losing_trades += 1

    # Afficher les statistiques
    print(f"Total Trades: {total_trades}, Win Rate: {calculate_win_rate()}%")

# Fonction pour calculer l'EMA
def calculate_ema(data, period):
    return pd.Series(data).ewm(span=period, adjust=False).mean().iloc[-1]

# Fonction pour gérer les ticks dans un thread séparé pour chaque symbole
def manage_ticks(symbol):
    ema_periods = symbols_params[symbol]["ema_periods"]
    ticks_queue = deque(maxlen=ema_periods[-1])  # Max period pour ce symbole
    print(f"Récupération des ticks pour {symbol}...")
    i = 0
    while True:
        last_tick = mt5.symbol_info_tick(symbol)
        if last_tick is None:
            print(f"Erreur lors de la récupération des ticks pour {symbol}.")
        else:
            if symbol == "BTCUSD":
                i += 1
                print(f"Tick {i}")
                
            ticks_queue.append(last_tick.bid)

            # Calculer les EMA pour ce symbole
            if len(ticks_queue) >= ema_periods[-1]:
                ema_values[symbol] = [calculate_ema(list(ticks_queue), period) for period in ema_periods]

            time.sleep(1)

def manage_trades(symbol):
    while True:
        if None not in ema_values[symbol]:  # Si toutes les EMA sont calculées
            ema60, ema120, ema180, ema240 = ema_values[symbol]
            if not positions_ouvertes[symbol]:
                last_tick = mt5.symbol_info_tick(symbol)
                if last_tick is None:
                    print(f"Erreur lors de la récupération des ticks pour {symbol}.")
                    break

                pips = symbols_params[symbol]["pips"]
                lot_size = lot_sizes[symbol]
                ratio = symbols_params[symbol]["ratio"]

                # Buy signal
                if ema60 > ema120 and ema120 > ema180 and ema180 > ema240 and last_tick.bid > ema60:
                    print(f"Signal d'achat détecté pour {symbol}.")
                    tp = last_tick.ask + (pips * ratio)  # Objectif de profit
                    stop_loss = last_tick.ask - pips  # Stop loss
                    result = open_buy_order(symbol, lot_size, tp, stop_loss)

                    if result is None:
                        print(f"Erreur : impossible d'ouvrir une position pour {symbol}. Résultat: {result}")
                        continue  # Ne pas aller plus loin si l'ouverture échoue

                    if result.retcode == mt5.TRADE_RETCODE_DONE:
                        print(f"Ordre d'achat exécuté avec succès pour {symbol}.")
                        positions_ouvertes[symbol] = True
                        order_thread = threading.Thread(target=track_order, args=(symbol, result.order,))
                        order_thread.daemon = True
                        order_thread.start()
                    else:
                        print(f"Erreur lors de l'ouverture de la position pour {symbol} : {result.comment}")

                # Sell signal
                elif ema60 < ema120 and ema120 < ema180 and ema180 < ema240 and last_tick.bid < ema60:
                    print(f"Signal de vente détecté pour {symbol}.")
                    tp = last_tick.bid - (pips * ratio)  # Objectif de profit
                    stop_loss = last_tick.bid + pips  # Stop loss
                    result = open_sell_order(symbol, lot_size, tp, stop_loss)

                    if result is None:
                        print(f"Erreur : impossible d'ouvrir une position pour {symbol}. Résultat: {result}")
                        continue  # Ne pas aller plus loin si l'ouverture échoue

                    if result.retcode == mt5.TRADE_RETCODE_DONE:
                        print(f"Ordre de vente exécuté avec succès pour {symbol}.")
                        positions_ouvertes[symbol] = True
                        order_thread = threading.Thread(target=track_order, args=(symbol, result.order,))
                        order_thread.daemon = True
                        order_thread.start()
                    else:
                        print(f"Erreur lors de l'ouverture de la position pour {symbol} : {result.comment}")

        time.sleep(1)

# Fonction pour suivre l'ordre par symbole
def track_order(symbol, order_id):
    global lot_sizes

    print(f"Suivi de l'ordre {order_id} en cours pour {symbol}...")
    order_result = bot.bot_order_tracking2(order_id)

    # Gérer le résultat de l'ordre
    if order_result == "TP":
        lot_sizes[symbol] = symbols_params[symbol]["initial_lot"]
        update_profit_and_stats("TP")
        print(f"TP -> LOT initial pour {symbol}: ", lot_sizes[symbol])
    elif order_result == "SL":
        lot_sizes[symbol] *= 2
        update_profit_and_stats("SL")
        print(f"SL -> LOT x2 pour {symbol}: ", lot_sizes[symbol])
    else:
        print(f"Erreur ou position non trouvée pour {symbol}.")

    positions_ouvertes[symbol] = False


# Lancer la gestion des ticks et des trades pour chaque symbole
for symbol in symbols_params.keys():
    ticks_thread = threading.Thread(target=manage_ticks, args=(symbol,))
    ticks_thread.start()

    trade_thread = threading.Thread(target=manage_trades, args=(symbol,))
    trade_thread.start()
    
        # Ajouter les threads à la liste pour utiliser join plus tard
    threads.append(ticks_thread)
    threads.append(trade_thread)

# Utiliser join après avoir démarré tous les threads
for thread in threads:
    thread.join()
