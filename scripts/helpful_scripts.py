from brownie import network, accounts, config
LIVE_NETWORKS = ["Sepolia"]

def get_account(i = 0):
    if network.show_active() in LIVE_NETWORKS:
        return accounts.add(config["wallets"]["key" + str(i)])
    else:
        return accounts[i]
    
def get_publish_source():
    return config["networks"][network.show_active()]["verify"]