import requests, time, json
import sqlite3


def redundancia0(b):
    try:
        r = requests.get(f'https://dubcheckers.gq/search/?bin={b}').text

        r = json.loads(r)

        tipo = r['type']
        level = r['nivel']
        banco = r['banco']
        pais = r['pais']
        bandeira = r['bandeira']

        return bandeira, tipo, level, banco, pais

    except: 
        return '', '', '', '', ''


def redundancia3(b):
    try:
        r = requests.get(f'http://140.82.31.167/search/bin={b}').text

        r = json.loads(r)

        tipo = r['type']
        level = r['nivel']
        banco = r['banco']
        pais = r['pais']
        bandeira = r['bandeira']

        return bandeira, tipo, level, banco, pais
        
    except:
        return '', '', '', '', ''


def redundancia1(b):
    try:
        r = requests.get(f'https://bin-checker.net/api/{b}').json()
        bandeira = r['scheme']
        tipo = r['type']
        level = r['level']
        banco = r['bank']['name']
        pais = r['country']['name']

        return bandeira, tipo, level, banco, pais
    
    except:
        return '', '', '', '', ''


def redundancia2(b):
    try:
        r = requests.get(f'https://lookup.binlist.net/{b}').json()
        try:
            bandeira = str(r['scheme']).replace('None', '').upper()
        except:
            bandeira = ''
        
        try:
            tipo = str(r['type']).replace('None', '').upper()
        except:
            tipo = ''
        
        try:
            level = str(r['brand']).replace('None', '').upper()
        except:
            level = ''
        
        try:
            banco = str(r['bank']['name']).replace('None', '').upper()
        except:
            banco = ''
        
        try:
            pais = str(r['country']['name']).replace('None', '').upper()
        except:
            pais = ''

        return bandeira, tipo, level, banco, pais
    
    except:
        return '', '', '', '', ''



def redundancia4(b):
    try:
        r = requests.get('https://bin-check-dr4g.herokuapp.com/api/'+b).text
        load = json.loads(r)['data']

        banco = load['bank']
        bandeira = load['vendor']
        level = load['level']
        if bandeira == 'HIPERCARD':
            level = 'HIPERCARD'
        if level == '':
            level = 'INDEFINIDO'
        tipo = load['type']
        pais = load['country']
        
        return banco, bandeira, level, tipo, pais

    except:
        return '', '', '', '', ''



def bin_checker(bi):
    a = redundancia1(bi)
    b = redundancia2(bi)

    if not a[0] == '':
        bandeira = a[0]
    
    elif not b[0] == '' or not b[0] == 'AMEX':
        bandeira = b[0]

    else:
        bandeira = ''

    
    if not a[1] == '':
        tipo = a[1]
    
    elif not b[1] == '':
        tipo  = b[1]

    else:
        tipo = ''


    if a[0] == 'AMERICAN EXPRESS' or b[0] == 'AMERICAN EXPRESS':
        level = 'AMERICAN EXPRESS'

    elif not a[2] == '':
        level = a[2]
    
    elif not b[2] == '':
        level  = b[2]

    else:
        level = ''
    
    if not a[3] == '':
        banco = a[3]
    
    elif not b[3] == '':
        banco  = b[3]

    else:
        banco = ''

    if not a[4] == '':
        pais = a[4]
    
    elif not b[4] == '':
        pais  = b[4]

    if level == 'INDEFINIDO' or level == '':
        pais = ''
        a = redundancia0(bi)
        pais = a[4]
        bandeira = a[0]
        tipo = a[1]
        level = a[2]
        banco = a[3]

        if level == 'INDEFINIDO' or level == '':
            principal = redundancia3(bi)
            
            level = principal[2]
            bandeira = principal[0]
            banco = principal[3]
            tipo = principal[1]
            pais = principal[4]


    return bandeira, tipo, level, banco, pais

