from typing import Callable


def costumer_repository_outside_port(customer_adapter_repository: dict) -> Callable[[tuple], tuple]:

    def create(customer: tuple) -> tuple:
        return customer_adapter_repository["create"](customer)

    return create
