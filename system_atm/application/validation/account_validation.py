import re


def account_validation():

    pattern_name = r'^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$'

    def isFloat(value):
        try:
            return True if float(value) else False
        except:
            return False

    def check_fields(account_num: str, name: str, balance: str) -> dict:

        occurrences: dict = {}

        

        if account_num not in ("1", "2", "3"):

            occurrences.update(
                {"account_num": "Selecione uma conta válida"})

        if len(name) < 10:
            occurrences.update(
                {"name": "Nome deve possuir no mínimo 10 caracteres"})

        elif re.match(pattern_name, name) is None:

            occurrences.update(
                {"name": "Nome deve possuir apenas caracteres válidos"})

        if isFloat(balance) is False:

            occurrences.update(
                {"balance": "Informe um saldo correto"})

        return occurrences

    return check_fields
