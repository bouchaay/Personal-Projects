# Stop loss sur pourcentage de loss depuis l'equity
def stop_loss_percent(symbol, current_price, balance, percent, lot, ordre):
    
    # Normaliser le pourcentage
    loss = balance*(percent/100)
    
    # Stop loss pour le Gold
    if symbol == "XAUUSD":
        if ordre == "s":
            return current_price + (loss/(lot*100))
        else:
            return current_price - (loss/(lot*100))
    
    # Stop loss pour le Bitcoin
    if symbol == "BTCUSD":
        if ordre == "s":
            return current_price + (loss/lot)
        else:
            return current_price - (loss/lot)

    # Stop loss pour l'Ethereum
    if symbol == "ETHUSD":
        if ordre == "s":
            return current_price + (loss/lot)
        else:
            return current_price - (loss/lot)
    
    # Stop loss pour les autres devises
    if ordre == "s":
        return current_price + (loss/(lot*100000))
    else :
        return current_price - (loss/(lot*100000))