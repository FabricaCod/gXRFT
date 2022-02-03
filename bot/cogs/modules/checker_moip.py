import requests, json, random
from fordev.generators import people



def create_order():
    rand = str(random.randint(00000000000, 99999999999))
    with open('assets/db_emails.json', 'r') as file2:
        load = json.loads(file2.read())
        emails = load['emails']
        email = random.choice(emails)
    url = 'https://api.moip.com.br/v2/orders'
    dados = people()
    nome = dados["nome"].upper()
    preco = random.randint(100, 200)
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic U0daRThKTklXS0FNVDRHT1dLVFRET0NCUTEzUDVJMUM6TkJMU1pWNjZPTzdKT1ExT1hTVk1FS1dYQU5MUkZDMkNWVlJKNjRFWA=='}


    data = {  
        "ownId": rand,
        "items": [
            {
            "product": rand,
            "quantity": 1,
            "detail": rand,
            "price": preco
            }
        ],
        "customer": {
            "ownId": "cliente"+rand,
            "fullname": nome,
            "email": email
        }
        }

    response = requests.post(url,headers=headers,json=data).json()

    return response['id']


def moip(cc):
    if len(cc.split("|")) == 4:
        numero, mes, ano, cvv = cc.split('|')
        if len(ano) == 2:
            ano = '20'+ano
        
        dados = people()
        paymenyid = create_order()

        url = 'https://api.moip.com.br/v2/orders/'+paymenyid+'/payments'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic U0daRThKTklXS0FNVDRHT1dLVFRET0NCUTEzUDVJMUM6TkJMU1pWNjZPTzdKT1ExT1hTVk1FS1dYQU5MUkZDMkNWVlJKNjRFWA=='}

        data = {
            "installmentCount":1,
            "fundingInstrument":{
                "method":"CREDIT_CARD",
                "creditCard":{
                "expirationMonth": mes,
                "expirationYear": ano,
                "cvc": cvv,
                "number": numero,
                "holder":{
                    "fullname":dados["nome"].upper(),
                    "birthdate":dados["data_nasc"].split("/"),
                    "taxDocument":{
                    "type":"CPF",
                    "number":dados["cpf"]
                    },
                    "phone":{
                    "countryCode":"55",
                    "areaCode":str(random.randint(10, 90)),
                    "number":dados["celular"].replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
                    }
                }
                }
            }
            }

        response = requests.post(url,headers=headers,json=data).text

        return response



print(moip('5534500641486017|12|2027|473'))
