from typing import Callable


def get_account_service(costumer_repository_port: Callable[[tuple], tuple]) -> Callable[[tuple], tuple]:

    def create(customer: tuple) -> tuple:
        return costumer_repository_port(customer)

    return create
