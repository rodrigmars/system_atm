from typing import Callable


def create_new_customer_service(costumer_repository_outside_port: Callable[[tuple], tuple]) -> Callable[[tuple], tuple]:

    def create(customer: tuple) -> tuple:
        return costumer_repository_outside_port(customer)

    return create
