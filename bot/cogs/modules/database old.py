from time import time
from random import sample
import sqlite3, requests



try:
    conn = sqlite3.connect('database.db', check_same_thread=False, isolation_level=None, timeout=30000)
    conn.rollback()
    conn.close()
except:
    pass

try:        
    conn = sqlite3.connect('database.db', check_same_thread=False, isolation_level=None, timeout=30000)
    cur = conn.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS cc (cc_id text, numero text, expiracao text, cvv text, tipo text, bandeira text, categoria text, banco text, pais text, cpf text, nome text, comprador text, hora text);")
    cur.execute("CREATE TABLE IF NOT EXISTS cc_comprada (cc_id text, numero text, expiracao text, cvv text, tipo text, bandeira text, categoria text, banco text, pais text, cpf text, nome text, comprador text, hora text);")
    cur.execute("CREATE TABLE IF NOT EXISTS usuarios (id_user text, saldo text, nome text, hora text);")
    cur.execute("CREATE TABLE IF NOT EXISTS recarga (id_user text, saldo_adicionado text, order_id text, hora text);")
    cur.execute("CREATE TABLE IF NOT EXISTS precos (categoria text, preco text);")
    cur.execute("CREATE TABLE IF NOT EXISTS afiliados (afiliado text, indicado text, hora text);")
    cur.execute("CREATE TABLE IF NOT EXISTS configs (variavel text, condicao text);")
    cur.execute("CREATE TABLE IF NOT EXISTS mix (quantidade text, preco text);")
    cur.execute("CREATE TABLE IF NOT EXISTS administrador (id_user text);")
    cur.execute("CREATE TABLE IF NOT EXISTS gifts (gift text, valor text, id_user text, hora text);")
    cur.execute("CREATE TABLE IF NOT EXISTS grupos (id_group, hora text);")
    cur.execute("CREATE TABLE IF NOT EXISTS cc_chk (numero text, expiracao text, cvv text, tipo text, bandeira text, categoria text, banco text, pais text, nome text, result text, retorno text, hora text);")
    cur.execute("CREATE TABLE IF NOT EXISTS cc_die (cc text, hora text);")
    cur.execute("CREATE TABLE IF NOT EXISTS banned (id_user text, hora text);")


except Exception as e:
    print('\nErro na conexão com o servidor do SQLite3\n\nLog do erro:', e)
    exit()



def pesquisar_ban(pesquisar):
    try:
        sql = 'SELECT * FROM banned WHERE id_user = ?'
        row = cur.execute(sql,  (pesquisar,))
        row = cur.fetchone()
        return row

    except:
        return None


def registrar_ban(user_id):
    if pesquisar_ban(user_id) == None:
        hora = str(time())
        cur.execute(f'INSERT INTO banned (id_user, hora) VALUES (?,?)', (user_id, hora,))
        conn.commit()


def remove_ban(user_id):
    try:
        if not pesquisar_ban(user_id) == None:
            sql = 'DELETE FROM banned WHERE id_user = ?'
            cur.execute(sql,  (user_id,))
            conn.commit()
            
            return True

        else:
            return False

    except:
        return False


def check_config(pesquisar):
    contador = 0
    while True:
        contador += 1
        if not contador > 5:
            try:
                sql = 'SELECT * FROM configs WHERE variavel = ?'
                row = cur.execute(sql,  (pesquisar,))
                row = cur.fetchone()
                break
            
            except:
                pass
            
        else:
            row = ['', '1']
            break

        
    return row


def add_config(variavel, condicao):
    check = check_config(variavel)
    if check is None:
        cur.execute(f'INSERT INTO configs (variavel, condicao) VALUES (?,?)', (variavel, condicao))
        conn.commit()



def check_group(pesquisar):
    sql = 'SELECT * FROM grupos WHERE id_group = ?'
    row = cur.execute(sql,  (pesquisar,))
    row = cur.fetchone()

    return row


def check_comprada(pesquisar):
    sql = 'SELECT * FROM cc_comprada WHERE numero = ?'
    row = cur.execute(sql,  (pesquisar,))
    row = cur.fetchone()

    if row is None:
        return True
    
    else:
        remove_cc(pesquisar, False)
        return False


def add_group(id_group):
    check = check_group(id_group)
    if check is None:
        hora = str(time())
        cur.execute(f'INSERT INTO grupos (id_group, hora) VALUES (?,?)', (id_group, hora,))
        conn.commit()
        
        return True
    
    else:
        return False


def config_change(variavel, condicao):
    cur.execute(
        "UPDATE configs SET condicao = (?)"
        "WHERE variavel = (?)", (condicao, variavel,))

    conn.commit()


def check_cc_database(pesquisar):
    try:
        sql = 'SELECT * FROM cc WHERE numero = ?'
        row = cur.execute(sql,  (pesquisar,))
        row = cur.fetchone()
        return row
    
    except:
        return None


def level_price(pesquisar):
    try:
        sql = 'SELECT * FROM precos WHERE categoria = ?'
        row = cur.execute(sql,  (pesquisar.upper(),))
        row = cur.fetchone()
        if row == None:
            return None

        else:
            if row[1] == 'None':
                return 'Não especificado'
            
            else:
                return row[1]
    except:
        return 'Não especificado'


def price_change(level, preco):
    cur.execute(
        "UPDATE precos SET preco = (?)"
        "WHERE categoria = (?)", (preco, level.upper(),))

    conn.commit()


def add_level(level):
    sql = 'SELECT * FROM precos WHERE categoria = ?'
    row = cur.execute(sql,  (level,))
    row = cur.fetchone()
    if row == None:
        preco = 'None'
        cur.execute(f'INSERT INTO precos (categoria, preco) VALUES (?,?)', (level, preco))
        conn.commit()


def check_level():
    try:
        cur.execute("""select * from "precos";""")
        row = cur.fetchone()
        
        results= []
        while row is not None:
            preco = row[1]
            if preco == 'None':
                results.append(preco)
            
            row = cur.fetchone()
            
        return len(results)

    except:
        return 0


def name_update(id_user, nome_atual):
    try:
        sql = 'SELECT * FROM usuarios WHERE id_user = ?'
        row = cur.execute(sql,  (id_user,))
        row = cur.fetchone()
        if row is not None:
            nome_registrado = row[2]
            if nome_registrado == nome_atual.strip():
                pass

            else:
                cur.execute(
                    "UPDATE usuarios SET nome = (?)"
                    "WHERE id_user = (?)", (nome_atual.strip(), id_user,))

    except:
        pass


def pesquisar_adm(pesquisar):
    try:
        if not pesquisar_ban(pesquisar) is None:
            sql = 'SELECT * FROM administrador WHERE id_user = ?'
            row = cur.execute(sql,  (pesquisar,))
            row = cur.fetchone()
            return row

        else:
            return None

    except:
        return None


def registrar_adm(user_id):
    if pesquisar_adm(user_id) == None:
        cur.execute(f'INSERT INTO administrador (id_user) VALUES (?)', (user_id,))
        conn.commit()


def remove_adm(user_id):
    try:
        if not pesquisar_adm(user_id) == None:
            sql = 'DELETE FROM administrador WHERE id_user = ?'
            cur.execute(sql,  (user_id,))
            conn.commit()
            
            return True

        else:
            return False

    except:
        return False


def remove_cc(numero, die=True):
    try:
        sql = 'SELECT * FROM cc WHERE numero = ?'
        cur.execute(sql,  (numero,))
        row = cur.fetchone()
        expiracao = str(row[2]).replace('/', '|20')
        cvv = row[3]
        
        cc = f'{numero}|{expiracao}|{cvv}'
        
        sql = 'DELETE FROM cc WHERE numero = ?'
        cur.execute(sql,  (numero,))
        conn.commit()
        
        if die:
            hora = str(time())
            cur.execute(f'INSERT INTO cc_die (cc, hora) VALUES (?,?)', (cc, hora))
            conn.commit()

        sql = 'DELETE FROM cc WHERE numero = ?'
        cur.execute(sql,  (numero,))
        conn.commit()

        return True
    except:
        return False


def all_groups():
    results= []
    
    try:
        cur.execute("""select * from "grupos";""")
        row = cur.fetchone()
        while row is not None:
            results.append(row[0])
            row = cur.fetchone()
    except:
        pass
    
    return results

def all_adms():
    results= []
    
    try:
        cur.execute("""select * from "administrador";""")
        row = cur.fetchone()
        while row is not None:
            results.append(row[0])
            row = cur.fetchone()
    except:
        pass

    return results



def pesquisar_id(pesquisar):
    contador = 0
    while True:
        contador += 1
        if not contador >5:
            try:
                sql = 'SELECT * FROM usuarios WHERE id_user = ?'
                row = cur.execute(sql,  (pesquisar,))
                row = cur.fetchone()
                break
            except:
                pass
        
        else:
            row = None
            break
    
    return row


def registrar_usuario(user_id, nome):
    if pesquisar_id(user_id) == None:
        saldo = '0'
        hora = str(time())
        cur.execute(f'INSERT INTO usuarios (id_user, saldo, nome, hora) VALUES (?,?,?,?)', (user_id, saldo, nome, hora))
        conn.commit()


def registrar_recarga(id_user, saldo, order_id):
    pesquisa = pesquisar_id(id_user)
    if not pesquisa == None:
        hora = str(time())
        cur.execute(f'INSERT INTO recarga (id_user, saldo_adicionado, order_id, hora) VALUES (?,?,?,?)', (id_user, saldo, order_id, hora))
        conn.commit()


def ccs_comprados(id_user):
    try:
        sql = 'SELECT * FROM cc WHERE comprador = ?'
        row = cur.execute(sql,  (id_user,))
        row = cur.fetchone()
        results1= []
        while row is not None:
            results1.append(row)
            row = cur.fetchone()

        sql = 'SELECT * FROM cc_comprada WHERE comprador = ?'
        row = cur.execute(sql,  (id_user,))
        row = cur.fetchone()
        results2= []
        while row is not None:
            results2.append(row)
            row = cur.fetchone()
        
        results = results1+results2
        
        return len(results)

    except:
        return 0


def recargas(id_user):
    try:
        sql = 'SELECT * FROM recarga WHERE id_user = ?'
        row = cur.execute(sql,  (id_user,))
        row = cur.fetchone()
        results= []
        while row is not None:
            results.append(row)
            row = cur.fetchone()

        return len(results)

    except:
        return 0


def add_saldo(id_user, saldo):
    saldo_atual = pesquisar_id(id_user)
    if saldo_atual is not None:
        soma = str(int(saldo_atual[1])+int(saldo))
        cur.execute("UPDATE usuarios SET saldo = (?)""WHERE id_user = (?)", (soma, id_user,))
        conn.commit()


def subtrair_saldo(id_user, saldo):
    saldo_atual = pesquisar_id(id_user)
    if saldo_atual is not None:
        if not int(saldo_atual[1]) < int(saldo):
            subtracao = str(int(saldo_atual[1])-int(saldo))
        else:
            subtracao = '0'

        cur.execute("UPDATE usuarios SET saldo = (?)""WHERE id_user = (?)", (subtracao, id_user,))
        conn.commit()


def rate_limit_chk(id_user, reset):
    check = pesquisar_id(id_user)
    if not reset:
        if check is not None:
            sql = 'SELECT * FROM limit_chk WHERE id_user = ?'
            row = cur.execute(sql,  (id_user,))
            row = cur.fetchone()
            if row is None:
                rate_init = '0'
                cur.execute(f'INSERT INTO limit_chk (id_user, rate) VALUES (?,?)', (id_user, rate_init,))
                conn.commit()
                
                return False
            
            else:
                if int(row[1]) >= 4:
                    rate = str(int(row[1]) + 1)
                    cur.execute("UPDATE limit_chk SET rate = (?)""WHERE id_user = (?)", (rate, id_user,))
                    conn.commit()
                    return False
                
                else:
                    rate = '0'
                    cur.execute("UPDATE limit_chk SET rate = (?)""WHERE id_user = (?)", (rate, id_user,))
                    conn.commit()
                    return True
    else:
        rate = '0'
        cur.execute("UPDATE limit_chk SET rate = (?)""WHERE id_user = (?)", (rate, id_user,))
        conn.commit()
        return False


def cadastrar_cartao(cc_id, numero, expiracao, cvv, tipo, bandeira, categoria, banco, pais, cpf, nome, comprador, data):
    cur.execute(f'INSERT INTO cc (cc_id, numero, expiracao, cvv, tipo, bandeira, categoria, banco, pais, cpf, nome, comprador, hora) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', (cc_id, numero, expiracao, cvv, tipo, bandeira, categoria, banco, pais, cpf, nome, comprador, data,))
    conn.commit()


def all_precos():
    results= []
    
    try:
        cur.execute("""select * from "precos";""")
        row = cur.fetchone()
        
        while row is not None:
            results.append(row)
            row = cur.fetchone()

    except:
        pass

    return results


def pesquisar_categoria(categoria):
    results = []
    
    try:
        ccs = all_ccs()
        
        for row in ccs:
            comprador = row[11]
            hora = row[12]
            if categoria == row[6]:
                results.append(row)
    
    except:
        pass

    return results


def pesquisar_cc_id(cc_id):
    try:
        sql = 'SELECT * FROM cc WHERE cc_id = ?'
        cur.execute(sql,  (cc_id,))
        row = cur.fetchone()
        
        return row
    
    except:
        return None


def check_afiliado(id_user_indicado):
    sql = 'SELECT * FROM afiliados WHERE indicado = ?'
    row = cur.execute(sql,  (id_user_indicado,))
    row = cur.fetchone()

    if not row == None:
        return row[0]

    else:
        return None


def add_afiliado(id_user_afiliado, id_user_indicado):
    row = pesquisar_id(id_user_afiliado)
    
    if not row == None:
        if not id_user_indicado == id_user_afiliado:
            if check_afiliado(id_user_indicado) == None:
                if pesquisar_id(id_user_indicado) is None:
                    hora = str(time())
                    cur.execute(f'INSERT INTO afiliados (afiliado, indicado, hora) VALUES (?,?,?)', (id_user_afiliado, id_user_indicado, hora))
                    conn.commit()


def comissao(id_user, saldo):
    afiliado = check_afiliado(id_user)
    if not afiliado == None:
        calculo = int(saldo) - int(int(saldo) * (1 - 10 / 100))
        add_saldo(str(afiliado), calculo)
        
        return True
    
    else:
        return False


def lista_indicados(id_user_afiliado):
    try:
        sql = 'SELECT * FROM afiliados WHERE afiliado = ?'
        row = cur.execute(sql,  (id_user_afiliado,))
        row = cur.fetchone()

        results= []
        while row is not None:
            indicado = row[1]
            results.append(indicado)
            row = cur.fetchone()

        return len(results)

    except:
        return 0


def update_cartao(cc_id, user_id, hora):
    try:
        remove_cc(numero)
        
        user_id = str(user_id)
        cc_id = str(cc_id)
        hora = str(hora)
        row = pesquisar_cc_id(cc_id)
        numero = row[1]
        expiracao = row[2]
        cvv = row[3]
        tipo = row[4]
        bandeira = row[5]
        categoria = row[6]
        banco = row[7]
        pais = row[8]
        cpf = row[9]
        nome = row[10]
        comprador = user_id
        hora = str(time())
        
        cur.execute(f'INSERT INTO cc_comprada (cc_id, numero, expiracao, cvv, tipo, bandeira, categoria, banco, pais, cpf, nome, comprador, hora) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', (cc_id, numero, expiracao, cvv, tipo, bandeira, categoria, banco, pais, cpf, nome, user_id, hora,))
        conn.commit()

        return True

    except:
        return False


def precos(tipo):
    try:
        sql = 'SELECT * FROM precos WHERE categoria = ?'
        row = cur.execute(sql,  (tipo,))
        row = cur.fetchone()
        return row[1]
    
    except:
        return 'Indefinido'


def buscar_preco(categoria, lista):
    def corte_preco(c):
        contador = -1
        n = 0
        for l in c:
            contador += 1
            if l.isnumeric():
                n = contador
                break
            
        return n

    for c in lista:
        if not c.find(categoria.upper().strip()) == -1:
            corte = corte_preco(c)
            return c[corte:]


def precos_inline():
    try:
        results = []
        sql = 'SELECT * FROM precos'
        row = cur.execute(sql,)
        row = cur.fetchone()
        
        while row is not None:
            if not row[1] == 'None':
                results.append(row[0]+' '+row[1])
            row = cur.fetchone()
        
        return results
    
    except:
        return []


def all_ccs_compradas():
    try:
        sql = 'SELECT * FROM cc_comprada'
        cur.execute(sql)
        row = cur.fetchone()

        results = []
        while row is not None:
            results.append(row)

            row = cur.fetchone()
            
        return results

    except Exception as e:
        print(e)
        return []



def all_ccs():
    try:
        lista = list(precos_inline())
        comprador = 'None'
        sql = 'SELECT * FROM cc WHERE comprador = ?'
        cur.execute(sql,  (str(comprador),))
        row = cur.fetchone()

        results = []
        while row is not None:
            categoria = row[6]
            p = buscar_preco(categoria, lista)
            if not p == None:
                results.append(row)

            row = cur.fetchone()
            
        return results

    except Exception as e:
        print(e)
        return []




def all_ccs_added():
    lista = list(precos_inline())
    comprador = 'None'
    sql = 'SELECT * FROM cc'
    cur.execute(sql,)
    row = cur.fetchone()

    results = []
    while row is not None:
        categoria = row[6]
        if not row[12]=='None':
            p = buscar_preco(categoria, lista)
            if not p == None:
                results.append(row)

        row = cur.fetchone()
            
    return results


def all_dies():
    sql = 'SELECT * FROM cc_die'
    cur.execute(sql,)
    row = cur.fetchone()

    results = []
    while row is not None:
        results.append(row)
        row = cur.fetchone()
            
    return results


def pesquisar_info_categoria(categoria):
    try:
        sql = 'SELECT * FROM precos WHERE categoria = ?'
        row = cur.execute(sql,  (categoria,))
        row = cur.fetchone()
        
        return row

    except:
        return None


def pesquisar_comprador(user_id):
    try:
        sql = 'SELECT * FROM cc_comprada WHERE comprador = ?'
        cur.execute(sql,  (user_id,))
        row = cur.fetchone()
        cartoes = []
        
        while row is not None:
            cartoes.append(row)
            row = cur.fetchone()

        return cartoes

    except:
        return []


def pesquisar_recargas(user_id):
    try:
        sql = 'SELECT * FROM recarga WHERE id_user = ?'
        cur.execute(sql,  (user_id,))
        row = cur.fetchone()
        recargas = []
        
        while row is not None:
            recargas.append(row)
            row = cur.fetchone()

        return recargas

    except:
        return []


def excluir_conta(user_id):
    try:
        sql = "DELETE FROM usuarios WHERE id_user = ?"
        cur.execute(sql,  (user_id,))
        conn.commit()
        
        rows = pesquisar_recargas(user_id)
        for row in rows:
            order_id = row[2]
            sql = "DELETE FROM recarga WHERE order_id = ?"
            cur.execute(sql,  (order_id,))
            conn.commit()
        
        rows = pesquisar_comprador(user_id)
        for row in rows:
            cc_id = row[0]
            sql = "DELETE FROM cc WHERE cc_id = ?"
            cur.execute(sql,  (cc_id,))
            conn.commit()
            
        sql = 'DELETE FROM afiliados WHERE indicado = ?'
        cur.execute(sql,  (user_id,))
        conn.commit()
        
        while True:
            sql = 'DELETE FROM afiliados WHERE afiliado = ?'
            cur.execute(sql,  (user_id,))
            conn.commit()
            if row == None:
                break

        while True:
            sql = 'DELETE FROM gifts WHERE id_user = ?'
            cur.execute(sql,  (user_id,))
            conn.commit()
            if row == None:
                break

        sql = "DELETE FROM usuarios WHERE id_user = ?"
        cur.execute(sql,  (user_id,))
        conn.commit()
        return True

    except:
        return False


def gen_gift(valor):
    gift = ''
    while True:
        c_list = ['a','b','c','d','e','f','g','i','h','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','0']

        p1 = ''.join(sample(c_list, 5))
        p2 = ''.join(sample(c_list, 5))
        p3 = ''.join(sample(c_list, 5))
        p4 = ''.join(sample(c_list, 5))

        gift = f'{p1}-{p2}-{p3}-{p4}'
        
        sql = 'SELECT * FROM gifts WHERE gift = ?'
        row = cur.execute(sql,  (gift,))
        row = cur.fetchone()
        hora = 'None'

        if row == None:
            user = 'None'
            cur.execute(f'INSERT INTO gifts (gift, valor, id_user, hora) VALUES (?,?,?,?)', (gift, valor, user, hora))
            conn.commit()
            break

    return gift


def pesquisar_gift(pesquisar):
    try:
        sql = 'SELECT * FROM gifts WHERE gift = ?'
        row = cur.execute(sql,  (pesquisar,))
        row = cur.fetchone()
        return row

    except:
        return None


def pesquisar_gifts_resgatados(pesquisar):
    try:
        sql = 'SELECT * FROM gifts WHERE id_user = ?'
        row = cur.execute(sql,  (pesquisar,))
        row = cur.fetchone()
        
        results = []
        while row is not None:
            results.append(row)

            row = cur.fetchone()
            
        return results

    except:
        return []


def resgatar_gift(gift, id_user):
    p_gift = pesquisar_gift(gift)

    if p_gift is not None:
        user = p_gift[2]
        valor = p_gift[1]
        
        if user == 'None':
            hora = str(time())
            add_saldo(id_user, valor)
            cur.execute("UPDATE gifts SET id_user = (?)""WHERE gift = (?)", (id_user, gift,))
            conn.commit()
            cur.execute("UPDATE gifts SET hora = (?)""WHERE gift = (?)", (hora, gift,))
            conn.commit()
            return True, ''

        else:
            return False, '1'

    else:
        return False, '2'


def pesquisar_mix(quantidade):
    try:
        sql = 'SELECT * FROM mix WHERE quantidade = ?'
        row = cur.execute(sql,  (quantidade,))
        row = cur.fetchone()
        return row

    except:
        return None


def registrar_mix(quantidade, valor):
    pesquisa = pesquisar_mix(quantidade)
    if pesquisa is None:
        cur.execute(f'INSERT INTO mix (quantidade, preco) VALUES (?,?)', (quantidade, valor))
        conn.commit()


def all_mix():
    try:
        sql = 'SELECT * FROM mix'
        cur.execute(sql)
        row = cur.fetchone()

        results = []
        while row is not None:
            results.append(row)

            row = cur.fetchone()
            
        return results

    except:
        return []


def editar_valor_mix(quantidade, valor):
    cur.execute(
        "UPDATE mix SET preco = (?)"
        "WHERE quantidade = (?)", (valor, quantidade,))

    conn.commit()


def deletar_mix(quantidade):
    sql = "DELETE FROM mix WHERE quantidade = ?"
    cur.execute(sql,  (quantidade,))
    conn.commit()


def all_users_id():
    try:
        cur.execute("""select * from "usuarios";""")
        row = cur.fetchone()
        
        results= []
        
        while row is not None:
            results.append(row[0])
            row = cur.fetchone()

        return results

    except:
        return []


def all_users():
    try:
        cur.execute("""select * from "usuarios";""")
        row = cur.fetchone()
        
        results= []
        
        while row is not None:
            results.append(row)
            row = cur.fetchone()

        return results

    except:
        return []
