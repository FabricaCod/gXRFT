from bot.cogs.modules.checker_cielo import *
from bot.cogs.modules.checker_erede import *
from bot.cogs.modules.checker_pagarme import *
from bot.cogs.modules.checker_getnet import *
import json
from time import sleep


def checker(cc):
    with open('config/config_checker.json', 'r') as file:
        load = json.loads(file.read())
        gate = load['default']
    sleep(5)

    if gate == 'pagarme':
        check = pagarme(cc)

    elif gate == 'cielo':
        check = cielo(cc)

    elif gate == 'erede':
        check = erede(cc)

    elif gate == 'getnet':
        check = getnet(cc)
    
    else:
        check = ['Erro', 'Nenhum gate selecionado']
    
    return check

