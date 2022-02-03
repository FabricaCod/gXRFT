from pypix_static import create_pix_string_code
from decimal import Decimal
import json


def pix(valor):
    try:
        with open('config/config_pix.json', 'r') as file:
            config = json.loads(file.read())
            chave_pix = config['pix_key']

        receiver_params = {
            'key': chave_pix,
            'name': 'A',
            'city': 'SAO PAULO',
            'value': Decimal(f'{valor}.00'),
            }

        code = create_pix_string_code(**receiver_params)

        return code

    except:
        return 'Erro'





