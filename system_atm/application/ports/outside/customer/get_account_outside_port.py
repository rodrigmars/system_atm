from typing import Callable


def get_account_outside_port(customer_adapter_repository: dict) -> Callable[[tuple], tuple]:

    def find_by_account(account: tuple) -> tuple:
        return customer_adapter_repository["find_by_account"](account)

    return find_by_account
