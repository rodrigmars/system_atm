from typing import Callable


def create_customer_port(repository: dict) -> Callable[[tuple], None]:

    def create(customer: tuple) -> None:
        repository["create"](customer)

    return create
