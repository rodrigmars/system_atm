from domain.entities.customer import Customer

def customer_respository(repository: dict) -> dict:

    def create(customer: Customer) -> int:
        query = """
        INSERT INTO DADOS_BANCARIOS(NOME, CONTA, SALDO) \
            VALUES(:NOME, :CONTA, :SALDO)
        """
        return repository["execute"](query, (customer.nome, customer.conta, customer.saldo)).rowcount

    def find_by_id(id: int) -> tuple:

        return repository["fetchone"]("""
        SELECT * FROM DADOS_BANCARIOS WHERE ID=:ID
        """, (id, ))

    def find_by_account(bank_account: str):

        query = "SELECT CONTA FROM DADOS_BANCARIOS WHERE CONTA =:CONTA"

        return repository["fetchone"](query, (bank_account,))

    return {"create": create,
            "find_by_id": find_by_id,
            "find_by_account": find_by_account}
