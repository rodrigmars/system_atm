
def balance_repository_port(customer_adapter_repository: dict) -> dict:

    def check_balance(account: str) -> float:
        return customer_adapter_repository["check_balance"](account)

    def update_balance(account: str, balance: float) -> None:
        customer_adapter_repository["update_balance"](account, balance)

    return {"check_balance":check_balance, "update_balance":update_balance}