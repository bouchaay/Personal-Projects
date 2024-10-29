import tkinter as tk
from tkinter import messagebox, ttk
import MetaTrader5 as mt5
import meta_settings as ms
from market import *
from tracking_order import *
from strategies import *
import threading

def get_current_price(symbol, ordre):
    # Obtenir les informations sur le symbole
    tick = mt5.symbol_info_tick(symbol)
    
    # Vérifier si les informations sont valides
    if tick is None:
        print(f"Impossible d'obtenir le prix pour le symbole {symbol}")
        return None

    # Retourner le prix d'achat ou le prix de vente selon vos besoins
    return tick.ask if ordre == "b" else tick.bid

# Fonction pour afficher/masquer les champs selon le choix du stop loss
def update_stop_loss_fields():
    if stop_loss_choice.get() == 1:  # Saisie manuelle
        sl_label.grid()
        sl_entry.grid()
        percentage_label.grid_remove()
        percentage_entry.grid_remove()
    else:  # Calculé par pourcentage
        sl_label.grid_remove()
        sl_entry.grid_remove()
        percentage_label.grid()
        percentage_entry.grid()

def send_and_track_order():
    
    # Récupérer les valeurs des champs
    symbol = symbol_combobox.get()
    try:
        lot = float(lot_entry.get())
        tp1 = float(tp1_entry.get())
        tp2 = float(tp2_entry.get())
        tp3 = float(tp3_entry.get())
        tp4 = float(tp4_entry.get())
        
        # Récupérer l'ordre à partir des boutons radio
        ordre = 'b' if ordre_choice.get() == 1 else 's'

        if stop_loss_choice.get() == 1:  # Saisie manuelle
            stop_loss = float(sl_entry.get())
        else:  # Calculé en fonction du pourcentage
            percentage = float(percentage_entry.get())
            stop_loss = stop_loss_percent(symbol, get_current_price(symbol, ordre), mt5.account_info().balance, percentage, lot, ordre)

        if (tp1 >= tp2 or tp2 >= tp3 or tp3 >= tp4) and ordre == "b":
            messagebox.showerror("Erreur", "Les niveaux de take profit doivent être croissants pour un ordre d'achat.")
            return
        
        if (tp1 <= tp2 or tp2 <= tp3 or tp3 <= tp4) and ordre == "s":
            messagebox.showerror("Erreur", "Les niveaux de take profit doivent être décroissants pour un ordre de vente.")
            return
        
        if ordre == "b":
            result = open_buy_order(symbol, lot, tp4, stop_loss)
        else:  # ordre == "s"
            result = open_sell_order(symbol, lot, tp4, stop_loss)

        if result.retcode == mt5.TRADE_RETCODE_DONE:
            messagebox.showinfo("Succès", "Ordre exécuté avec succès")
            track_order(ordre, result.order, tp1, tp2, tp3)
        else:
            messagebox.showerror("Erreur", f"Erreur lors de l'exécution de l'ordre : {result.comment}")

    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")

def thread_send_order():
    order_thread = threading.Thread(target=send_and_track_order)
    order_thread.daemon = True
    order_thread.start()

# Se connecter à MetaTrader 5
ms.init_connect()
    
root = tk.Tk()
root.title("Ayex Trading Helper")

tk.Label(root, text="Symbole:").grid(row=0, column=0, padx=10, pady=10)
symbol_combobox = ttk.Combobox(root, values=["XAUUSD", "BTCUSD", "ETHUSD", "EURUSD", "USDCHF", "GBPUSD", "AUDUSD", "USDCAD", "NZDUSD", "USDJPY", "AUDNZD"])
symbol_combobox.grid(row=0, column=1, padx=10, pady=10)
symbol_combobox.set("XAUUSD")

tk.Label(root, text="Lot:").grid(row=1, column=0, padx=10, pady=10)
lot_entry = tk.Entry(root)
lot_entry.grid(row=1, column=1, padx=10, pady=10)

# Ajouter un titre pour les niveaux de TP
tp_title = tk.Label(root, text="Take Profit Levels", font=("Arial", 10))  # Réduire la taille de la police
tp_title.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

tk.Label(root, text="TP1:").grid(row=3, column=0, padx=10, pady=10)
tp1_entry = tk.Entry(root)
tp1_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="TP2:").grid(row=4, column=0, padx=10, pady=10)
tp2_entry = tk.Entry(root)
tp2_entry.grid(row=4, column=1, padx=10, pady=10)

tk.Label(root, text="TP3:").grid(row=5, column=0, padx=10, pady=10)
tp3_entry = tk.Entry(root)
tp3_entry.grid(row=5, column=1, padx=10, pady=10)

tk.Label(root, text="TP4:").grid(row=6, column=0, padx=10, pady=10)
tp4_entry = tk.Entry(root)
tp4_entry.grid(row=6, column=1, padx=10, pady=10)

# Ajouter un titre pour le Stop Loss
stop_loss_title = tk.Label(root, text="Configuration du Stop Loss", font=("Arial", 10))  # Réduire la taille de la police
stop_loss_title.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

stop_loss_choice = tk.IntVar(value=1)  # 1 pour manuel, 2 pour calculé
tk.Radiobutton(root, text="Manuel", variable=stop_loss_choice, value=1, command=update_stop_loss_fields).grid(row=8, column=0, padx=10, pady=5, sticky="w")
tk.Radiobutton(root, text="Pourcentage", variable=stop_loss_choice, value=2, command=update_stop_loss_fields).grid(row=8, column=1, padx=10, pady=5, sticky="w")

sl_label = tk.Label(root, text="Stop Loss:")
sl_label.grid(row=9, column=0, padx=10, pady=10)
sl_entry = tk.Entry(root)
sl_entry.grid(row=9, column=1, padx=10, pady=10)

percentage_label = tk.Label(root, text="Risque (%):")
percentage_label.grid(row=10, column=0, padx=10, pady=10)
percentage_entry = tk.Entry(root)
percentage_entry.grid(row=10, column=1, padx=10, pady=10)

# Ajouter un titre pour les boutons Buy/Sell
ordre_title = tk.Label(root, text="Buy/Sell Order", font=("Arial", 10))  # Réduire la taille de la police
ordre_title.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

# Ajouter des boutons radio pour Buy/Sell
ordre_choice = tk.IntVar(value=1)  # 1 pour acheter, 2 pour vendre
tk.Radiobutton(root, text="Buy", variable=ordre_choice, value=1).grid(row=12, column=0, padx=10, pady=5, sticky="w")
tk.Radiobutton(root, text="Sell", variable=ordre_choice, value=2).grid(row=12, column=1, padx=10, pady=5, sticky="w")

ok_button = tk.Button(root, text="OK", command=thread_send_order)
ok_button.grid(row=13, column=0, columnspan=2, padx=10, pady=10)

update_stop_loss_fields()  # Appeler cette fonction au démarrage pour cacher le champ selon la valeur par défaut

root.mainloop()