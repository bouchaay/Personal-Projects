import MetaTrader5 as mt5
import time
from market import *
import MetaTrader5 as mt5

sl_move_threshold_usd = 1  # Seuil de déplacement du stop loss en USD (pas de pips)

# Fonction poursuivre un ordre
def bot_order_tracking(order_id, order_type):
    # Traiter l'ordre de type achat
    if order_type == "b":
        while True:
            
            # Vérifier toutes les 1 secondes
            time.sleep(1)
            
            # Récupérer les détails de l'ordre ouvert
            position = mt5.positions_get(ticket=order_id)
            if position:
                pos = position[0]
                current_price = pos.price_current
                price_open = pos.price_open
                # Si on touche le SL on ferme la position
                if current_price <= pos.sl:
                    print("SL touché")
                    result = mt5.Close(symbol=pos.symbol, ticket=order_id)
                    if result == True:
                        print("Position fermée (SL touché).")
                        return "SL"
                    else:
                        print(f"Erreur lors de la fermeture de la position (SL)")
                        
                # Si on touche le TP on ferme la position
                if current_price >= pos.tp:
                    print("TP touché")
                    result = mt5.Close(symbol=pos.symbol, ticket=order_id)
                    if result == True:
                        print("Position fermée (TP touché).")
                        return "TP"
                    else:
                        print(f"Erreur lors de la fermeture de la position (TP)")
            else:
                order_info = mt5.history_orders_get(ticket=order_id)
                if order_info:
                    # Utiliser les informations de l'ordre
                    order = order_info[0]
                    print(order)
                    try:
                        if order.type == mt5.ORDER_TYPE_BUY:
                            current_price = mt5.symbol_info_tick(order.symbol).ask
                            profit = current_price - price_open
                        else:
                            current_price = mt5.symbol_info_tick(order.symbol).bid  # Obtenir le prix actuel
                            profit = price_open - current_price
                    except Exception as e:
                        print("Erreur lors de la récupération du prix actuel.")
                        print(e)
                        return "SL"

                    # Vérifier si le profit est positif ou négatif
                    if profit > 0:
                        return "TP"
                    else:
                        return "SL"
                else:
                    print("Aucune information d'ordre trouvée.")
            
    # Traiter l'ordre de type vente
    elif order_type == "s":
        while True:
            
            # Vérifier toutes les 1 secondes
            time.sleep(1)
            
            # Récupérer les détails de l'ordre ouvert
            position = mt5.positions_get(ticket=order_id)
            if position:
                pos = position[0]
                current_price = pos.price_current
                price_open = pos.price_open
                    
                # Si on touche le SL on ferme la position
                if current_price >= pos.sl:
                    print("SL touché")
                    result = mt5.Close(symbol=pos.symbol, ticket=order_id)
                    if result == True:
                        print("Position fermée (SL touché).")
                        return "SL"
                    else:
                        print(f"Erreur lors de la fermeture de la position (SL)")
                        
                # Si on touche le TP on ferme la position
                if current_price <= pos.tp:
                    print("TP touché")
                    result = mt5.Close(symbol=pos.symbol, ticket=order_id)
                    if result == True:
                        print("Position fermée (TP touché).")
                        return "TP"
                    else:
                        print(f"Erreur lors de la fermeture de la position (TP)")
            else:
                order_info = mt5.history_orders_get(ticket=order_id)
                if order_info:
                    # Utiliser les informations de l'ordre
                    order = order_info[0]
                    print(order)
                    try:
                        if order.type == mt5.ORDER_TYPE_BUY:
                            current_price = mt5.symbol_info_tick(order.symbol).ask
                            profit = current_price - price_open
                        else:
                            current_price = mt5.symbol_info_tick(order.symbol).bid  # Obtenir le prix actuel
                            profit = price_open - current_price
                    except Exception as e:
                        print("Erreur lors de la récupération du prix actuel.")
                        print(e)
                        return "SL"

                    # Vérifier si le profit est positif ou négatif
                    if profit > 0:
                        return "TP"
                    else:
                        return "SL"
                else:
                    print("Aucune information d'ordre trouvée.")
            
    
