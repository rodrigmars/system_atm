
from config import Connection, connect

from interface.main_menu import menu
import traceback

def create_tables() -> str:

    return """
    BEGIN;

    DROP TABLE DADOS_BANCARIOS;

    CREATE TABLE IF NOT EXISTS DADOS_BANCARIOS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        NOME TEXT NOT NULL,
        CONTA TEXT NOT NULL UNIQUE,
        SALDO NUMERIC NOT NULL,
        TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    COMMIT;
    """

class Customer:
    
    def __init__(self, nome: str, conta: str, saldo: float) -> None:

        self.nome = nome
        self.conta = conta
        self.saldo = saldo


def crete_customer(customer: Customer) -> tuple[str, tuple[str, str, float]]:
    return """
    INSERT INTO DADOS_BANCARIOS(NOME, CONTA, SALDO) VALUES(:NOME, :CONTA, :SALDO)
    """, (customer.nome, customer.conta, customer.saldo)


def find_by_id(id: int) -> tuple:
    return """
    SELECT * FROM DADOS_BANCARIOS WHERE ID=:ID
    """, (id, )


def main():

    conexao: Connection | None = None

    try:

        conexao = connect("Dados.db")

        cursor = conexao.cursor()

        cursor.executescript(create_tables())

        id = cursor.execute(*crete_customer(Customer("Vitória Bianca Viana", "38353-9", 150.0))).rowcount

        customer = cursor.execute(*find_by_id(id)).fetchone()

        conexao.commit()


        menu(conexao, cursor)

    except Exception:

        print(traceback.print_exc())

        if conexao:
            conexao.rollback()
    
    finally:

        if conexao:
            conexao.close()

if __name__ == "__main__":
    
    main()
