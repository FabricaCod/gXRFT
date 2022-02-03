import requests


token = ''
URL = "https://mb.api.pagseguro.uol/"

HTTP_HEADERS = {
    "user-agent":  "PagSeguro release/4.19.4 (br.com.uol.ps.myaccount; build:311; Android 8.1.0",
    "x-token": token
}

TYPES = ['PIX_RECEIVED', 'PIX_INTERNAL_TPZ', 'PIX_INTERNAL_IN']


def statement(days=1):
    if days:
        uri = f"/statement?daysBefore={days}"
    else:
        uri = f"/statement"

    statement = requests.get(
        url=URL + uri,
        headers=HTTP_HEADERS
    )

    if statement.status_code == 200:
        res = statement.json()
        statement.close()

        return res

    statement.close()

    return False


def transactions(days=1):
    if days:
        request = statement(days)
    else:
        request = statement()

    if not request or not 'statementCheckingAccount' in request:
        return False

    statementCheckingAccount = request['statementCheckingAccount']
    result = []

    for s in statementCheckingAccount:
        transactions = s['statementMovement']

        for t in transactions:
            if t['type'] in TYPES:
                result.append({
                    'checkingAccountOperationId': t['checkingAccountOperationId'],
                    'stepId': t['stepId'],
                    'value': t['value'].replace(u'R$\xa0', "").replace(',', '.')
                })

        return result

