from typing import Callable


def account_exists_inside_port(service: Callable[[tuple], tuple]) -> Callable[[tuple], tuple]:

    def check_account(account: tuple) -> tuple:
        return service(account)

    return check_account
