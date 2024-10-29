import tkinter as tk
from tkinter import messagebox
import threading
from tracking_order import *
import meta_settings as ms
import MetaTrader5 as mt5

# Initialiser MetaTrader 5
ms.init_connect()
    
# Initialiser la fenêtre principale
root = tk.Tk()
root.title("Application de Trading")

# Créer les champs d'entrée directement dans la fenêtre principale
tk.Label(root, text="Ticket de l'ordre:").grid(row=0, column=0, padx=10, pady=10)
ticket_entry = tk.Entry(root)
ticket_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="TP1:").grid(row=1, column=0, padx=10, pady=10)
tp1_entry = tk.Entry(root)
tp1_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="TP2:").grid(row=2, column=0, padx=10, pady=10)
tp2_entry = tk.Entry(root)
tp2_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="TP3:").grid(row=3, column=0, padx=10, pady=10)
tp3_entry = tk.Entry(root)
tp3_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="TP4:").grid(row=4, column=0, padx=10, pady=10)
tp4_entry = tk.Entry(root)
tp4_entry.grid(row=4, column=1, padx=10, pady=10)

tk.Label(root, text="SL:").grid(row=5, column=0, padx=10, pady=10)
sl_entry = tk.Entry(root)
sl_entry.grid(row=5, column=1, padx=10, pady=10)

def tracking_process():
    
    try:
        ticket = int(ticket_entry.get())
        tp1 = float(tp1_entry.get())
        tp2 = float(tp2_entry.get())
        tp3 = float(tp3_entry.get())
        tp4 = float(tp4_entry.get())
        sl = float(sl_entry.get())
        
        # Récupérer les détails de l'ordre
        position = mt5.positions_get(ticket=ticket)
        if not position:
            messagebox.showerror("Erreur", "Ordre introuvable.")
            return
        
        # Extraire les détails de l'ordre
        pos = position[0]
        
        # Déterminer la nature de l'ordre
        order_type = "b" if pos.type == mt5.ORDER_TYPE_BUY else "s"
        
        # Créer la requête pour changer le TP et le SL
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "symbol": pos.symbol,
            "sl": sl,  # Déplacer le SL au prix défini
            "tp": tp4,  # Déplacer le TP au niveau TP4
        }
        # Envoyer la requête
        result = mt5.order_send(request)
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            messagebox.showinfo("Succès", "Take profit et Stop loss changés.")
        else:
            messagebox.showerror("Erreur", f"Erreur lors de la mise à jour du TP et du SL : {result.comment}")
            return
        
        # Lancer le suivi de l'ordre
        track_order(order_type, ticket, tp1, tp2, tp3)
        messagebox.showinfo("Succès", "Suivi de l'ordre lancé.")
        
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")

def start_tracking_in_thread():
    # Démarrer le tracking dans un thread séparé
    tracking_thread = threading.Thread(target=tracking_process)
    tracking_thread.daemon = True
    tracking_thread.start()

# Ajouter le bouton OK pour démarrer le suivi directement dans la fenêtre principale
ok_button = tk.Button(root, text="OK", command=start_tracking_in_thread)
ok_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Lancer la boucle principale de l'interface
root.mainloop()
