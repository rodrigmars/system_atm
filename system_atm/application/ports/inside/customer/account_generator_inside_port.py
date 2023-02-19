from typing import Callable


def account_generator_inside_port(service: Callable[[], tuple]) -> Callable[[], tuple]:

    def check_account() -> tuple:
        return service()

    return check_account
