import MetaTrader5 as mt5
import pandas as pd

# Fonction pour envoyer l'ordre d'achat
def open_buy_order(symbol, lot, take_profit, stop_loss):
    order = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": mt5.symbol_info_tick(symbol).ask,
        "sl": stop_loss,
        "tp": take_profit,
        "comment": "Python script open buy order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
        "deviation": 100,
    }
    return mt5.order_send(order)

# Fonction pour envoyer l'ordre de vente
def open_sell_order(symbol, lot, take_profit, stop_loss):
    order = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": mt5.symbol_info_tick(symbol).bid,
        "sl": stop_loss,
        "tp": take_profit,
        "comment": "Python script open sell order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
        "deviation": 100,
    }
    return mt5.order_send(order)

def get_data(symbol, timeframe, num_bars):
    # Récupère les données OHLC de MetaTrader5
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    return data

