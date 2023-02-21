from typing import Callable


def create_new_customer_service(check_fields: Callable[[str, str, str], list],
                                costumer_repository_outside_port: Callable[[tuple], tuple]) -> Callable[[tuple], tuple]:

    def create(customer: tuple) -> tuple:

        num_account, name, balance, accounts = customer

        if (ocorrences := check_fields(num_account, name, balance)) != {}:

            return False, ocorrences, None

        else:

            account = [acc.get(int(num_account)) for acc in accounts if acc.get(
                int(num_account)) is not None][0]

            return True, {}, costumer_repository_outside_port((account, name, balance))

    return create
