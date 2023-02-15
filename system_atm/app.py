
import traceback

from config import Connection, connect

from interface.menu_adapter import menu
from domain.entities.customer import Customer
from infrastructure.repositories.customer_repository import customer_respository
from infrastructure.repositories.repository import repository

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

def main():

    conexao: Connection | None = None

    try:

        conexao = connect("Dados.db")

        cursor = conexao.cursor()

        cursor.executescript(create_tables())

        customer_repo = customer_respository(repository(cursor))

        id = customer_repo["create"](Customer("Vitória Bianca Viana", "38353-9", 150.0))

        customer = customer_repo["find_by_id"](id)

        print("customer", customer)

        conexao.commit()

        menu(cursor)

    except Exception:

        print(traceback.print_exc())

        if conexao:
            conexao.rollback()
    
    finally:

        if conexao:
            conexao.close()

if __name__ == "__main__":
    
    main()
