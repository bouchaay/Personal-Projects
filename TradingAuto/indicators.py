# Page pour les indicateurs techniques
#

# Importer les librairies
import numpy as np
from market import *
import pandas as pd

# Récupérer la tendance du marché pour une timeframe donnée et un nombre de périodes
def tendance_marche(symbol, timeframe, periods):
    # Récupérer les données du marché
    market_data = mt5.copy_rates_from_pos(symbol, timeframe, 0, periods)
    if market_data is None or len(market_data) < 2:
        return "Pas assez de données pour déterminer la tendance."
    df = pd.DataFrame(market_data)
    close_prices = df["close"].values
    time_indices = np.arange(len(close_prices))
    slope, _ = np.polyfit(time_indices, close_prices, 1)
    if slope > 0:
        return "tendance haussière"
    elif slope < 0:
        return "tendance baissière"
    else:
        return "neutre"
    
    