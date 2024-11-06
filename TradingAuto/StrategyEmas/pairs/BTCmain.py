import sys
import os

# Ajoute le chemin du dossier strategy à sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Remonte d'un niveau

import market as mk
import market as mk
import meta_settings as ms
import StrategyEmas.tracking_order_XAU as to
import MetaTrader5 as mt5
import threading
import time
        
initial_lot = 0.2
lot = initial_lot

def main():
    
    global position_ouverte, lot
    # Initialisation des variables
    position_ouverte = False
    symbol = 'BTCUSDm'
    attente = 1
    time_frame = mt5.TIMEFRAME_M1
    sl_max_usd = 50
    tp_static = 70     # Take 
    nb_bars = 30
    min_volume = 250
    
    # Connexion à MetaTrader 5
    ms.init_connect()
    
    while True:
        
        # Récupère les données OHLC
        data = mk.get_data(symbol, time_frame, nb_bars)
        
        # Calcul des EMA
        # Calcul des EMA et du volume moyen
        data['EMA30'] = data['close'].ewm(span=30, adjust=False).mean()
        data['EMA50'] = data['close'].ewm(span=50, adjust=False).mean()
        
        current_candle = data.iloc[-1]
        last_closed_candle = data.iloc[-2]
        previous_candle = data.iloc[-3]
        
        if not position_ouverte:
            
            buySignal = (previous_candle['EMA30'] < previous_candle['EMA50']) and \
                        (last_closed_candle['EMA30'] >= last_closed_candle['EMA50']) and \
                        (current_candle['EMA30'] > current_candle['EMA50']) and \
                        (current_candle['tick_volume'] >= min_volume)
                            
            # Si EMA20 < EMA30, on cherche une opportunité d'achat
            sellSignal = (previous_candle['EMA30'] > previous_candle['EMA50']) and \
                        (last_closed_candle['EMA30'] <= last_closed_candle['EMA50']) and \
                        (current_candle['EMA30'] < current_candle['EMA50']) and \
                        (current_candle['tick_volume'] >= min_volume)
            
            # Si une opportunité d'achat est détectée
            if buySignal:
                print("Buy signal detected")
                sl_buy = last_closed_candle['close'] - sl_max_usd
                tp_buy = last_closed_candle['close'] + tp_static
                result = mk.open_buy_order(symbol, lot, tp_buy, sl_buy)
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    position_ouverte = True
                    order_thread = threading.Thread(target=track_order, args=(result.order, "b"))
                    order_thread.daemon = True
                    order_thread.start()
                else:
                    print(f"Erreur lors de l'ouverture de la position : {result.comment}")
                    
            # Si une opportunité de vente est détectée
            elif sellSignal:
                print("Sell signal detected")
                sl_sell = last_closed_candle['close'] + sl_max_usd
                tp_sell = last_closed_candle['close'] - tp_static
                result = mk.open_sell_order(symbol, lot, tp_sell, sl_sell)
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    position_ouverte = True
                    order_thread = threading.Thread(target=track_order, args=(result.order, "s"))
                    order_thread.daemon = True
                    order_thread.start()
                else:
                    print(f"Erreur lors de l'ouverture de la position : {result.comment}")
                    
        time.sleep(attente)
        
def track_order(order, ordre):
    global position_ouverte, lot
    
    print(f"Suivi de l'ordre {order}")
    order_result = to.bot_order_tracking(order, ordre)
    print(f"Résultat de l'ordre: {order_result}")
    if order_result == "SL":
        lot = lot * 2
    else :
        lot = initial_lot
    position_ouverte = False
        
if __name__ == "__main__":
    main()