import tkinter as tk
from tkinter import messagebox, ttk
import MetaTrader5 as mt5
import meta_settings as ms
from market import *
from tracking_order import *
from strategies import *
import threading
import pandas as pd

ms.init_connect()

# Paramètres de l'instrument
symbol = "BTCUSD"
timeframe = mt5.TIMEFRAME_S1  # Timeframe d'une minute
pip_value = 0.10  # Ajustez selon la taille de votre position

# Fonction pour récupérer les données et appliquer la stratégie
def trade_strategy():
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 200)
    
    # Vérifier que les données ont été copiées
    if rates is None:
        print("Erreur lors de la récupération des données.")
        return
    
    df = pd.DataFrame(rates)

    # Imprimer les résultats de rates et df
    print("Données récupérées (rates) :")
    print(rates)
    print("\nDataFrame (df) :")
    print(df)

    # Calcul des EMA
    df['EMA21'] = df['close'].ewm(span=21, adjust=False).mean()
    df['EMA50'] = df['close'].ewm(span=50, adjust=False).mean()

    # Calcul de l'ATR
    df['high_low'] = df['high'] - df['low']
    df['high_close'] = abs(df['high'] - df['close'].shift(1))
    df['low_close'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)
    df['ATR'] = df['TR'].rolling(window=14).mean()

    # Vérifier les derniers signaux
    last_row = df.iloc[-1]

    # Vérifier les conditions d'achat et de vente
    if last_row['EMA21'] > last_row['EMA50']:
        print("Signal d'achat détecté")
        # Logique d'achat ici (ex: mt5.order_send())
    elif last_row['EMA21'] < last_row['EMA50']:
        print("Signal de vente détecté")
        # Logique de vente ici (ex: mt5.order_send())

# Boucle pour exécuter la stratégie régulièrement
while True:
    trade_strategy()
    time.sleep(60)  # Attendre 60 secondes avant de récupérer les nouvelles données