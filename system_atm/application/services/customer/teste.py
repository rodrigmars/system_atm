import random

def account_generator(get_account):

    accounts: list = []

    i: int = 0

    while i <= 2:

        if get_account((account := f"{random.randint(1, 99999):05}-{random.randint(1, 9)}",)) is None:
            i += 1
            accounts.append({i+1: account})

    return accounts




