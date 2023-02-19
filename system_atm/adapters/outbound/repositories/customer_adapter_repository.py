def customer_adapter_repository(repository: dict) -> dict:

    # CREATE TABLE IF NOT EXISTS BANK_DATA (
    #     ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    #     NAME TEXT NOT NULL,
    #     ACCOUNT TEXT NOT NULL UNIQUE,
    #     BALANCE NUMERIC NOT NULL,
    #     TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP
    # );

    def create(customer: tuple) -> tuple:
        query = """
        INSERT INTO BANK_DATA(NAME, ACCOUNT, BALANCE) \
            VALUES(:NAME, :ACCOUNT, :BALANCE)
        """
        return repository["execute"](query, customer).rowcount,

    def find_by_id(id: tuple) -> tuple:

        return repository["fetchone"]("""
        SELECT * FROM BANK_DATA WHERE ID=:ID
        """, id)

    def check_account(account: tuple) -> tuple:

        return repository["fetchone"]("""
        SELECT ACCOUNT FROM BANK_DATA WHERE ACCOUNT=:ACCOUNT
        """, account)

    def find_by_account(bank_account: tuple) -> tuple:

        query = "SELECT ACCOUNT FROM BANK_DATA WHERE ACCOUNT =:ACCOUNT"

        return repository["fetchone"](query, bank_account)

    def update_balance(account: str, balance: float) -> None:

        query = "UPDATE BANK_DATA SET BALANCE =:BALANCE WHERE ACCOUNT =:ACCOUNT"

        repository["execute"](query, (balance, account))

    return {"create": create,
            "find_by_id": find_by_id,
            "check_account": check_account,
            "find_by_account": find_by_account,
            "update_balance": update_balance}
