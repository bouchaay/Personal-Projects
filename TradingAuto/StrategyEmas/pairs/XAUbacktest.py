import sys
import os

# Ajoute le chemin du dossier strategy à sys.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # Remonte d'un niveau

import MetaTrader5 as mt5
import pandas as pd
import meta_settings as ms
import matplotlib.pyplot as plt

# Configuration
symbol = "XAUUSDm"
time_frame = mt5.TIMEFRAME_M1
sl_max_usd = 1.5  # Stop Loss maximum en USD #4
tp_static = 3  # Take Profit statique en USD #3
sl_move_threshold_usd = 1  # Seuil de déplacement du stop loss en USD (pas de pips)
multiplicateur_lot = 100
multiplier_after_loss = 1
initial_lot = 0.5
min_volume = 100


def backtest_strategy(jour, balance):
    
    balance_evol = []  # liste des valeurs de la balance
    nb_bars = (
        1440 * jour
    )  # Convertir les jours en nombre de barres pour timeframe de 1 minute

    # Connexion à MetaTrader 5
    ms.init_connect()

    # Récupération des données
    rates = mt5.copy_rates_from_pos(symbol, time_frame, int(0*(nb_bars//2)), nb_bars)
    data = pd.DataFrame(rates)
    data["time"] = pd.to_datetime(data["time"], unit="s")

    # Calcul des EMA
    data["EMA20"] = data["close"].ewm(span=20, adjust=False).mean()
    data["EMA30"] = data["close"].ewm(span=30, adjust=False).mean()

    position_ouverte = False
    total_profit = 0
    last_position_index = -1  # Pour suivre la dernière position ouverte
    win_count = 0  # Compteur de gains
    loss_count = 0  # Compteur de pertes
    consecutive_losses = 0  # Compteur de pertes consécutives
    max_consecutive_losses = 0  # Maximum de pertes consécutives
    max_drawdown = 0  # Maximum de perte en cours
    current_drawdown = 0  # Perte en cours
    lot = initial_lot
    nb_trade = 0
    nb_trade_buy = 0
    nb_trade_sell = 0
    nb_trade_buy_success = 0
    nb_trade_buy_loss = 0
    nb_trade_sell_success = 0
    nb_trade_sell_loss = 0

    # Variables BE
    be_count = 0  # Nombre de fois où le Stop Loss a été déplacé au point d'entrée
    be_hit_count = 0  # Nombre de fois où le Stop Loss déplacé a été touché

    # Commencer à partir de l'indice 30 pour garantir que les EMA sont calculées
    for i in range(30, len(data) - 1):
        if i <= last_position_index:
            continue  # Sauter si on est toujours sur une position ouverte

        # La dernière bougie clôturée
        current_candle = data.iloc[i]
        last_closed_candle = data.iloc[i - 1]
        previous_candle = data.iloc[i - 2]

        if not position_ouverte:
            # Détection des signaux d'achat et de vente
            buy_signal = (
                (previous_candle["EMA20"] < previous_candle["EMA30"])
                and (last_closed_candle["EMA20"] >= last_closed_candle["EMA30"])
                and (current_candle["EMA20"] > current_candle["EMA30"])
                and (current_candle["tick_volume"] >= min_volume)
            )
            sell_signal = (
                (previous_candle["EMA20"] > previous_candle["EMA30"])
                and (last_closed_candle["EMA20"] <= last_closed_candle["EMA30"])
                and (current_candle["EMA20"] < current_candle["EMA30"])
                and (current_candle["tick_volume"] >= min_volume)
            )

            # Ouverture d'une position d'achat
            if buy_signal:
                open_price = last_closed_candle["close"]
                sl_buy = open_price - sl_max_usd  # Stop Loss pour achat
                tp_buy = open_price + tp_static  # Take Profit statique
                position_ouverte = True
                last_position_index = i
                nb_trade += 1
                nb_trade_buy += 1

                # Vérification des conditions de fermeture de position
                for j in range(i + 1, len(data)):
                    current_price = data.iloc[j]["close"]

                    # Suivi du Stop Loss à Break Even
                    if (
                        current_price >= open_price + sl_move_threshold_usd
                        and sl_buy != open_price
                    ):  # Si le prix évolue de 1.5 USD
                        sl_buy = (
                            open_price  # Déplacer le SL au point d'entrée (Break Even)
                        )
                        be_count += 1  # Compter le BE atteint

                    if (
                        current_price <= sl_buy
                    ):  # Si le Stop Loss est touché après le déplacement
                        position_ouverte = False
                        if (
                            sl_buy == open_price
                        ):  # Si le SL est touché après le déplacement
                            be_hit_count += 1
                        else:
                            profit = abs(
                                (open_price - sl_buy) * lot * multiplicateur_lot
                            )
                            balance -= profit
                            total_profit -= profit
                            loss_count += 1
                            consecutive_losses += 1
                            max_consecutive_losses = max(
                                max_consecutive_losses, consecutive_losses
                            )
                            lot *= multiplier_after_loss
                            current_drawdown += sl_max_usd * lot * multiplicateur_lot
                            max_drawdown = max(max_drawdown, current_drawdown)
                            nb_trade_buy_loss += 1
                        balance_evol.append(balance)
                        break
                    elif current_price >= tp_buy:
                        position_ouverte = False
                        profit = abs((tp_buy - open_price) * lot * multiplicateur_lot)
                        total_profit += profit
                        balance += profit
                        win_count += 1
                        consecutive_losses = 0
                        lot = initial_lot
                        current_drawdown = 0
                        nb_trade_buy_success += 1
                        balance_evol.append(balance)
                        break
                last_position_index = j

            # Ouverture d'une position de vente
            elif sell_signal:
                open_price = last_closed_candle["close"]
                sl_sell = open_price + sl_max_usd
                tp_sell = open_price - tp_static
                position_ouverte = True
                last_position_index = i
                nb_trade += 1
                nb_trade_sell += 1

                for j in range(i + 1, len(data)):
                    current_price = data.iloc[j]["close"]

                    # Suivi du Stop Loss à Break Even
                    if (
                        current_price <= open_price - sl_move_threshold_usd
                        and sl_sell != open_price
                    ):  # Si le prix évolue de 1.5 USD
                        sl_sell = (
                            open_price  # Déplacer le SL au point d'entrée (Break Even)
                        )
                        be_count += 1  # Compter le BE atteint

                    if (
                        current_price >= sl_sell
                    ):  # Si le Stop Loss est touché après le déplacement
                        position_ouverte = False
                        if (
                            sl_sell == open_price
                        ):  # Si le SL est touché après le déplacement
                            be_hit_count += 1
                        else:
                            profit = abs(
                                (open_price - sl_sell) * lot * multiplicateur_lot
                            )
                            total_profit -= profit
                            balance -= profit
                            loss_count += 1
                            consecutive_losses += 1
                            max_consecutive_losses = max(
                                max_consecutive_losses, consecutive_losses
                            )
                            lot *= multiplier_after_loss
                            current_drawdown += sl_max_usd * lot * multiplicateur_lot
                            max_drawdown = max(max_drawdown, current_drawdown)
                            nb_trade_sell_loss += 1
                        balance_evol.append(balance)
                        break
                    elif current_price <= tp_sell:
                        position_ouverte = False
                        profit = abs((tp_sell - open_price) * lot * multiplicateur_lot)
                        total_profit += profit
                        balance += profit
                        win_count += 1
                        consecutive_losses = 0
                        lot = initial_lot
                        current_drawdown = 0
                        nb_trade_sell_success += 1
                        balance_evol.append(balance)
                        break
                last_position_index = j

    # Calcul des statistiques finales
    total_trades = win_count + loss_count
    win_rate = (win_count / total_trades * 100) if total_trades > 0 else 0
    be_win_rate = (
        (be_hit_count / be_count * 100) if be_count > 0 else 0
    )  # Win rate pour BE

    return {
        "jour": jour,
        "total_profit": total_profit,
        "win_rate": win_rate,
        "be_win_rate": be_win_rate,  # Ajout du win rate pour BE
        "max_consecutive_losses": max_consecutive_losses,
        "max_drawdown": max_drawdown,
        "nb_trade": nb_trade,
        "nb_trade_buy": nb_trade_buy,
        "nb_trade_sell": nb_trade_sell,
        "nb_trade_buy_success": nb_trade_buy_success,
        "nb_trade_buy_loss": nb_trade_buy_loss,
        "nb_trade_sell_success": nb_trade_sell_success,
        "nb_trade_sell_loss": nb_trade_sell_loss,
        "be_count": be_count,  # Nombre de fois où le BE a été atteint
        "be_hit_count": be_hit_count,
        "balance": balance,
    }, balance_evol


# Boucle pour tester différents jours
if __name__ == "__main__":
    balance = 1000  # Balance initiale
    results = []
    for jour in range(1, 2):  # De 1 jour à 31 jours
        result, balance_evol = backtest_strategy(jour, balance)
        results.append(result)
        print(
            f"Day: {result['jour']} \nTotal Profit: {result['total_profit']} USD\n"
            f"Win Rate: {result['win_rate']:.2f}%\n"
            f"Max consecutive losses: {result['max_consecutive_losses']}\n"
            f"Max drawdown: {result['max_drawdown']} USD\n"
            f"Number of trades: {result['nb_trade']}\n"
            f"Number of buy orders: {result['nb_trade_buy']}\n"
            f"Number of sell orders: {result['nb_trade_sell']}\n"
            f"Number of successful buy order: {result['nb_trade_buy_success']}\n"
            f"Number of losing buy order: {result['nb_trade_buy_loss']}\n"
            f"Number of successful sell order: {result['nb_trade_sell_success']}\n"
            f"Number of losing sell order: {result['nb_trade_sell_loss']}\n"
            f"BE count: {result['be_count']}\n"
            f"BE hit count: {result['be_hit_count']}\n"
            f"Balance: {result['balance']} USD\n"
        )

        if jour == 1:
            balance = result["balance"]
            print(f"Final balance: {balance} USD\n")

            # Affichage de l'évolution de la balance lissée
            plt.plot(range(len(balance_evol)), balance_evol, label="Balance")

            # Définir les limites de l'axe des x et y
            plt.xlim(0, len(balance_evol))
            plt.yticks(range(int(min(balance_evol)) - 100, int(max(balance_evol)) + 100, 100))

            # Ajouter des labels et un titre pour améliorer la lisibilité
            plt.xlabel("Bougie")
            plt.ylabel("Balance (USD)")
            plt.title("Évolution de la balance lissée")
            plt.grid(True)
            # Affichage du graphique
            plt.show()
