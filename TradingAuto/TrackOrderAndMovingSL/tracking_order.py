import MetaTrader5 as mt5
import time
from market import *
import MetaTrader5 as mt5

# Fonction pour suivre un ordre
def track_order(order_type, order_id, tp1, tp2, tp3):
    
    # Pour éviter de déplacer le SL plusieurs fois
    tp1_reached = False
    tp2_reached = False
    tp3_reached = False
    
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
            
                # Si on touche le SL on ferme la position
                if current_price <= pos.sl:
                    result = mt5.Close(symbol=pos.symbol, ticket=order_id)
                    if result == True:
                        print("Position fermée (SL touché).")
                        break
                    else:
                        print(f"Erreur lors de la fermeture de la position (SL) : {result.comment}")
            
                # Si on atteint le TP1
                if current_price >= tp1 and not tp1_reached:
                    request_tp1 = {
                        "action": mt5.TRADE_ACTION_SLTP,
                        "position": order_id,
                        "symbol": pos.symbol,
                        "sl": pos.price_open,  # Déplacer le SL au prix d'entrée
                        "tp": pos.tp,  # Garder le TP inchangé
                    }
                    # Envoyer la requête
                    result_tp1 = mt5.order_send(request_tp1)
                    if result_tp1.retcode == mt5.TRADE_RETCODE_DONE:
                        print("Stop loss déplacé au niveau de break-even.")
                        tp1_reached = True
                    else:
                        print(f"Erreur lors de la mise à jour du stop loss au BE : {result_tp1.comment}")
                    
                # Si on atteint le TP2
                if current_price >= tp2 and not tp2_reached:
                    request_tp2 = {
                        "action": mt5.TRADE_ACTION_SLTP,
                        "position": order_id,
                        "symbol": pos.symbol,
                        "sl": tp1,  # Déplacer le SL au niveau de TP précédent
                        "tp": pos.tp,  # Garder le TP inchangé
                    }
                    # Envoyer la requête
                    result_tp2 = mt5.order_send(request_tp2)
                    if result_tp2.retcode == mt5.TRADE_RETCODE_DONE:
                        print("Stop loss déplacé au niveau de TP1.")
                        tp2_reached = True
                    else:
                        print(f"Erreur lors de la mise à jour du stop loss au TP1 : {result_tp2.comment}")
                    
                # Si on atteint le TP3
                if current_price >= tp3 and not tp3_reached:
                    request_tp3 = {
                        "action": mt5.TRADE_ACTION_SLTP,
                        "position": order_id,
                        "symbol": pos.symbol,
                        "sl": tp2,  # Déplacer le SL au niveau de TP précédent
                        "tp": pos.tp,  # Garder le TP inchangé
                    }
                    # Envoyer la requête
                    result_tp3 = mt5.order_send(request_tp3)
                    if result_tp3.retcode == mt5.TRADE_RETCODE_DONE:
                        print("Stop loss déplacé au niveau de TP2.")
                        tp3_reached = True
                    else:
                        print(f"Erreur lors de la mise à jour du stop loss au TP2 : {result_tp3.comment}")
                    
                # Si on atteint le TP4
                if current_price >= pos.tp:
                    result = mt5.Close(symbol=pos.symbol, ticket=order_id)
                    if result == True:
                        print("Position fermée (TP4 touché).")
                        break
                    else:
                        print(f"Erreur lors de la fermeture de la position (TP) : {result.comment}")
            else:
                print("Position introuvable ou fermée.")
                return
            
    # Traiter l'ordre de type vente
    if order_type == "s":
        while True:
            
            # Vérifier toutes les 1 secondes
            time.sleep(1)
            
            # Récupérer les détails de l'ordre ouvert
            position = mt5.positions_get(ticket=order_id)
            if position:
                pos = position[0]
                current_price = pos.price_current
            
                # Si on touche le SL on ferme la position
                if current_price >= pos.sl:
                    result = mt5.Close(symbol=pos.symbol, ticket=order_id)
                    if result == True:
                        print("Position fermée (SL touché).")
                        break
                    else:
                        print(f"Erreur lors de la fermeture de la position (SL) : {result.comment}")
            
                # Si on atteint le TP1
                if current_price <= tp1 and not tp1_reached:
                    request_tp1 = {
                        "action": mt5.TRADE_ACTION_SLTP,
                        "position": order_id,
                        "symbol": pos.symbol,
                        "sl": pos.price_open,  # Déplacer le SL au prix d'entrée
                        "tp": pos.tp,  # Garder le TP inchangé
                    }
                    # Envoyer la requête
                    result_tp1 = mt5.order_send(request_tp1)
                    if result_tp1.retcode == mt5.TRADE_RETCODE_DONE:
                        print("Stop loss déplacé au niveau de break-even.")
                        tp1_reached = True
                    else:
                        print(f"Erreur lors de la mise à jour du stop loss au BE : {result_tp1.comment}")
                    
                # Si on atteint le TP2
                if current_price <= tp2 and not tp2_reached:
                    request_tp2 = {
                        "action": mt5.TRADE_ACTION_SLTP,
                        "position": order_id,
                        "symbol": pos.symbol,
                        "sl": tp1,  # Déplacer le SL au niveau de TP précédent
                        "tp": pos.tp,  # Garder le TP inchangé
                    }
                    # Envoyer la requête
                    result_tp2 = mt5.order_send(request_tp2)
                    if result_tp2.retcode == mt5.TRADE_RETCODE_DONE:
                        print("Stop loss déplacé au niveau de TP1.")
                        tp2_reached = True
                    else:
                        print(f"Erreur lors de la mise à jour du stop loss au TP1 : {result_tp2.comment}")
                    
                # Si on atteint le TP3
                if current_price <= tp3 and not tp3_reached:
                    request_tp3 = {
                        "action": mt5.TRADE_ACTION_SLTP,
                        "position": order_id,
                        "symbol": pos.symbol,
                        "sl": tp2,  # Déplacer le SL au niveau de TP précédent
                        "tp": pos.tp,  # Garder le TP inchangé
                    }
                    # Envoyer la requête
                    result_tp3 = mt5.order_send(request_tp3)
                    if result_tp3.retcode == mt5.TRADE_RETCODE_DONE:
                        print("Stop loss déplacé au niveau de TP2.")
                        tp3_reached = True
                    else:
                        print(f"Erreur lors de la mise à jour du stop loss au TP2 : {result_tp3.comment}")
                    
                # Si on atteint le TP4
                if current_price <= pos.tp:
                    result = mt5.Close(symbol=pos.symbol, ticket=order_id)
                    if result == True:
                        print("Position fermée (TP4 touché).")
                        break
                    else:
                        print(f"Erreur lors de la fermeture de la position (TP) : {result.comment}")
            else:
                print("Position introuvable ou fermée.")
                return
            
    
