from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.cogs.modules.import_text_variables import *
from bot.cogs.modules.database import *
from bot.cogs.modules.support import *
from bot.cogs.modules.checker import *
import asyncio
import random


def is_null(content):
    if content.strip() == '' or content.strip() == 'None':
        return 'N/A'
    else:
        return content
    
    
def cc_usada(cc):
    if not os.path.isfile('temp/compradas'):
        with open('temp/compradas', 'w', encoding='UTF-8') as file:
            file.write('')
            
    with open('temp/compradas', 'a', encoding='UTF-8') as file:
        file.write(str(cc)+'\n')



def a_cc_foi_usada(cc):
    if not os.path.isfile('temp/compradas'):
        with open('temp/compradas', 'w', encoding='UTF-8') as file:
            file.write('')
            
    with open('temp/compradas', 'r', encoding='UTF-8') as file:
        data = file.read()
        if cc in data:
            return True
        else:
            return False


def choose_cc(level):
    rows = asyncio.run(pesquisar_categoria(level))
    q = len(rows)
    if not q == 0:
        if q > 0:
            row = list(rows[random.randint(0, len(rows)-1)])

            if asyncio.run(check_comprada(row[1])):
                return True, row
            else:
                row = []
            
            if rows == []:
                return False, []

        else:
            return False, []

    else:
        return False, []


def troca(update: Update, context: CallbackContext):
    query = update.callback_query
    user_info = query.from_user
    user_id = str(user_info['id'])

    level = query.data.split('|')[1]
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'💳 | *Escolhendo outro cartão...*\n\nOutro cartão está sendo escolhido...', parse_mode='Markdown')

    while True:
        contador_die = 0
        contador_die += 1
        repetidos = []
        try:
            if not contador_die >= 20:
                cc = choose_cc(level)
                if cc[0] or not cc[1] == []:
                    row = cc[1]
                    cc_id = cc[0]
                    numero = row[1]
                    expiracao = is_null(row[2])
                    cvv = is_null(row[3])
                    tipo = is_null(row[4])
                    bandeira = is_null(row[5])
                    categoria = is_null(row[6])
                    banco = is_null(row[7])
                    cpf = is_null(row[9])
                    nome = is_null(row[10])
                    comprador = row[11]
                    hora = row[12]
                    preco_cc = is_null(precos(categoria))
                
                    credit_card = f"{numero}|{expiracao.replace('/', '|')}|{cvv}"
                    if not credit_card in repetidos:
                        repetidos.append(credit_card)
                        check = checker(credit_card)
                        print(check)
                        if check[0] == True and not a_cc_foi_usada(credit_card):
                            cc_usada(credit_card)
                            saldo = asyncio.run(pesquisar_id(user_id))[1]
                            if int(preco_cc) <= int(saldo):
                                update_cc = asyncio.run(update_cartao(cc_id, user_id, hora))

                                asyncio.run(subtrair_saldo(user_id, preco_cc))
                                status = f'\n\n✅ *Status*: `#Aprovado - Retorno: {check[1]}`'

                                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=cc_info.format(numero, expiracao, cvv, bandeira, tipo, categoria, banco, cpf, nome, preco_cc)+status, parse_mode='Markdown')
                                
                            else:
                                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f'💳 | *O cartão não pode ser comprado por saldo insuficiente!*\n\nO cartão não foi comprado por você já não ter mais o saldo na carteira para isso, provavelmente porque o saldo da sua carteira foi usado para compra de outra CC nesse meio tempo. Contate o suporte caso esse seja um mal entendido!', parse_mode='Markdown')

                            break
                            

                        else:
                            asyncio.run(remove_cc(numero))

                else:
                    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='💳 | *CCs equivalentes acabaram!*\n\nNão foi possível realizar a troca, pois as ccs do nível especifico acabaram. Tente entrar em contato com o suporte caso seja necessário resolver o problema!', parse_mode='Markdown')
                    break

            else:
                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='💳 | *Limite ultrrapassado!*\n\nDemorou muito tempo desde a sua compra, por favor, tente novamente ou chame o suporte caso o problema percista!', parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
                break
            
        except Exception as e:
            context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='💳 | *O Cartão não pode ser trocado!*\n\nTente escolher outra CC ou chame o suporte caso o problema percista!', parse_mode='Markdown')
            break











