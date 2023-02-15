
import traceback

from config import Connection, connect

from interface.menu_adapter import menu
from infrastructure.repositories.customer_repository import customer_repository
from infrastructure.repositories.repository import repository
from application.usercases.customer.create_user_case import create_customer_user_case
from application.usercases.customer.get_account_user_case import get_account_user_case
from application.usercases.customer.execute_transfer_use_case import execute_transfer_use_case


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

        customer_repo = customer_repository(repository(cursor))

        menu(get_account_user_case(customer_repo),
             execute_transfer_use_case(customer_repo),
             create_customer_user_case(customer_repo))

    except Exception:

        traceback.print_exc()

        if conexao:
            conexao.rollback()
    
    finally:

        if conexao:
            conexao.close()

if __name__ == "__main__":
    
    main()
