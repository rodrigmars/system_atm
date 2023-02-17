from typing import Callable


def get_account_inside_port(service: Callable[[tuple], tuple]) -> Callable[[tuple], tuple]:

    def find_by_account(account: tuple) -> tuple:
        return service(account)

    return find_by_account
