def customer_adapter_repository(repository: dict) -> dict:

    def create(customer: tuple) -> int:
        query = """
        INSERT INTO DADOS_BANCARIOS(NOME, CONTA, SALDO) \
            VALUES(:NOME, :CONTA, :SALDO)
        """
        return repository["execute"](query, customer).rowcount

    def find_by_id(id: int) -> tuple:

        return repository["fetchone"]("""
        SELECT * FROM DADOS_BANCARIOS WHERE ID=:ID
        """, (id, ))

    def find_by_account(bank_account: str) -> str:

        query = "SELECT CONTA FROM DADOS_BANCARIOS WHERE CONTA =:CONTA"

        return repository["fetchone"](query, (bank_account,))

    def update_balance(account: str, balance: float) -> None:

        query = "UPDATE DADOS_BANCARIOS SET SALDO =:SALDO WHERE CONTA =:CONTA"

        repository["execute"](query, (balance, account))

    return {"create": create,
            "find_by_id": find_by_id,
            "find_by_account": find_by_account,
            "update_balance": update_balance}