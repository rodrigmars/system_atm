from typing import Callable


def account_exists_service(account_exists_outside_port: Callable[[tuple], tuple]) -> Callable[[tuple], tuple]:

    def account_exists(account: tuple) -> tuple:

        return account_exists_outside_port(account)

    return account_exists
