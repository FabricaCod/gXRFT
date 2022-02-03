import stripe




stripe.api_key = "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"


def tokenization(cc):
    numero, mes, ano, cvv = '', 0, 0, ''
    if len(cc.split("|")) == 4:
        numero, mes, ano, cvv = cc.split('|')
    if len(ano) == 2:
        ano = '20'+ano
        
    card = stripe.Token.create(card={"number": numero, "exp_month": int(mes), "exp_year": int(ano), "cvc": cvv})

    return card


print(tokenization('5162926018480631|10|2028|511'))

