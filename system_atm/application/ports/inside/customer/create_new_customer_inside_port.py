from typing import Callable


def create_new_customer_inside_port(service: Callable[[tuple], int]) -> Callable[[tuple], int]:

    def create(customer: tuple) -> int:
        return service(customer)

    return create
