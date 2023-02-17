from typing import Callable

def execute_transfer_service(balance_repository_use_case: dict) -> Callable[[str, str, float], str]:

    # def check_balance(account: str) -> float:
    #     return balance_repository_use_case["check_balance"](account)

    # def update_balance(account: str, balance: float) -> None:
    #     balance_repository_use_case["update_balance"](account, balance)


    def make_transfer(primary_account: str, secondary_account: str, valor_transferencia: float) -> str:

        saldo = balance_repository_use_case["check_balance"](primary_account)

        if saldo >= valor_transferencia:

            valor_debitado = saldo - valor_transferencia

            balance_repository_use_case["update_balance"](primary_account, valor_debitado)

            balance_repository_use_case["update_balance"](secondary_account,
                           balance_repository_use_case["check_balance"](secondary_account) + valor_transferencia)

            return "Transferência executada com sucesso!"

        else:
            return "Saldo insuficiente!"

    return make_transfer
