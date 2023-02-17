from typing import Callable


def execute_transfer_port(repository: dict) -> Callable[[str, str, float], str]:

    def check_balance(account: str) -> float:
        return repository["check_balance"](account)

    def update_balance(account: str, balance: float) -> None:
        repository["update_balance"](account, balance)

    def make_transfer(primary_account: str, secondary_account: str, valor_transferencia: float) -> str:

        saldo = check_balance(primary_account)

        if saldo >= valor_transferencia:

            valor_debitado = saldo - valor_transferencia

            update_balance(primary_account, valor_debitado)

            update_balance(secondary_account,
                           check_balance(secondary_account) + valor_transferencia)

            return "Transferência executada com sucesso!"

        else:
            return "Saldo insuficiente!"

    return make_transfer
