import MetaTrader5 as mt5
import account_infos as ai

# Initialiser MetaTrader 5
def init():
    if not mt5.initialize():
        print("Initialisation a échouée.")
        mt5.shutdown()
        quit()
        return False
    else:
        return True
        
        
# Se connecter à un compte
def connect(username, password, server):
    account = mt5.login(login=int(username), password=password, server=server)
    if account:
        return True
    else:
        print("Login échoué.")
        mt5.shutdown()
        quit()
        return False
    
# Se connecter à MetaTrader 5
def init_connect():
    if not init():
        return False
    if not connect(ai.username, ai.password, ai.server):
        return False
    return True
