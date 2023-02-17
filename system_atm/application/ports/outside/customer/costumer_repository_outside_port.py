from typing import Callable


def costumer_repository_outside_port(customer_adapter_repository: dict) -> Callable[[tuple], int]:

    def create(customer: tuple) -> int:
        print(">>>>>>>>>>>>>>>2", tuple)
        return customer_adapter_repository["create"](customer)

    return create
