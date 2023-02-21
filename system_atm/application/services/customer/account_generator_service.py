from typing import Callable
import random


def account_generator_service(get_account_inside_outside_port: Callable[[tuple], tuple]) -> Callable[[], tuple]:

    def account_generator() -> tuple:
        """
        Account Generator

        Função para geração de novas contas

        Returns
        -------
        tuple

        Example
        --------
        >>> account_generator()
        ("00001-1", "00002-1", "00003-1")
        """

        accounts: list = []

        i: int = 0

        while i <= 2:

            if get_account_inside_outside_port((account := f"{random.randint(1, 99999):05}-{random.randint(1, 9)}",)) is None:
                i += 1
                accounts.append({i: account})

        return tuple(accounts)

    return account_generator
