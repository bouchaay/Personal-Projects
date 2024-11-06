import MetaTrader5 as mt5
import time

# Fonction pour suivre un ordre
def bot_order_tracking(order_id):
    res = "PNF"
    while True:
        # Vérifier toutes les 1 secondes
        time.sleep(1)

        # Récupérer les détails de l'ordre ouvert
        position = mt5.positions_get(ticket=order_id)
        if position:
            pos = position[0]
            current_price = pos.price_current

            profit = pos.profit
            print(f"Profit : {profit}")
            
            # si position d'achat
            if pos.type == mt5.ORDER_TYPE_BUY:
                # Si on atteint le TP
                if current_price >= pos.tp:
                    result = True #mt5.Close(symbol=pos.symbol, ticket=order_id)
                    if result:
                        print("TP")
                        res = "TP"
                    else:
                        print("Échec de la fermeture de la position (TP).")
                    break
                    
                # Si on atteint le SL
                if current_price <= pos.sl:
                    result = True #mt5.Close(symbol=pos.symbol, ticket=order_id)
                    if result:
                        print("SL")
                        res = "SL"
                    else:
                        print("Échec de la fermeture de la position (SL).")
                    break

            # si position de vente
            elif pos.type == mt5.ORDER_TYPE_SELL:
                # Si on atteint le TP
                if current_price <= pos.tp:
                    result = True#mt5.Close(symbol=pos.symbol, ticket=order_id)
                    if result:
                        print("TP")
                        res = "TP"
                    else:
                        print("Échec de la fermeture de la position (TP).")
                    break
                    
                # Si on atteint le SL
                if current_price >= pos.sl:
                    result = True#mt5.Close(symbol=pos.symbol, ticket=order_id)
                    if result:
                        print("SL")
                        res = "SL"
                    else:
                        print("Échec de la fermeture de la position (SL).")
                    break
        
        else:
            print(res)  # Afficher le résultat avant de sortir
            return res

    print(res)  # Afficher le résultat final
    return res




def bot_order_tracking2(order_id):
    res = "PNF"
    while True:
        # Vérifier toutes les 1 secondes
        time.sleep(1)

        # Récupérer les détails de l'ordre
        position = mt5.positions_get(ticket=order_id)
        if position:
            pos = position[0]
            profit = pos.profit
            price_open = pos.price_open
            print(f"Profit : {profit}")
            
        else:
            #print("Position fermée.")
            order_info = mt5.history_orders_get(ticket=order_id)
            if order_info:
                # Utiliser les informations de l'ordre
                order = order_info[0]

                try:
                    if order.type == mt5.ORDER_TYPE_BUY:
                        current_price = mt5.symbol_info_tick(order.symbol).ask
                        profit = current_price - price_open
                    else:
                        current_price = mt5.symbol_info_tick(order.symbol).bid  # Obtenir le prix actuel
                        profit = price_open - current_price
                except:
                    print("Erreur lors de la récupération du prix actuel.")
                    return "SL"

                # Vérifier si le profit est positif ou négatif
                if profit > 0:
                    res = "TP"
                else:
                    res = "SL"
            else:
                print("Aucune information d'ordre trouvée.")
                
            break
    return res


