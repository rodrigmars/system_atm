from typing import Callable

def get_account_inside_port(repository: dict) -> Callable[[str], str]:

    def find_by_account(account: str) -> str:
        return repository["find_by_account"](account)

    return find_by_account
