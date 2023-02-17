from typing import Callable


def create_new_customer_inside_port(service: Callable[[tuple], tuple]) -> Callable[[tuple], tuple]:

    def create(customer: tuple) -> tuple:
        return service(customer)

    return create
