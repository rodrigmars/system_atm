from typing import Callable


def account_exists_outside_port(customer_adapter_repository: dict) -> Callable[[tuple], tuple]:

    def check_account(account: tuple) -> tuple:
        return customer_adapter_repository["check_account"](account)

    return check_account
