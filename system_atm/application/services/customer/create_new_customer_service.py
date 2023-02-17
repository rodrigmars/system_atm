from typing import Callable


def create_new_customer_service(costumer_repository_port: Callable[[tuple], int]) -> Callable[[tuple], int]:

    def create(customer: tuple) -> int:
        print(">>>>>>>>>>>>>>>1", tuple)
        return costumer_repository_port(customer)

    return create
