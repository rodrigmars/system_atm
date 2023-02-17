
import traceback

from config import Connection, connect

from adapters.inbound.menu_adapter import menu

from adapters.outbound.repositories.customer_repository import customer_repository
from adapters.outbound.repositories.repository import repository
from application.ports.inside.customer.create_user_case import create_customer_user_case
from application.ports.inside.customer.get_account_user_case import get_account_user_case
from application.ports.inside.customer.execute_transfer_use_case import execute_transfer_use_case

def create_tables() -> str:

    return """
    BEGIN;

    DROP TABLE IF EXISTS DADOS_BANCARIOS;

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

        def container(repository: dict) -> tuple:

            return get_account_user_case(repository), \
                execute_transfer_use_case(repository), \
                create_customer_user_case(repository)

        menu(*container(customer_repo))

    except Exception:

        traceback.print_exc()

        if conexao:
            conexao.rollback()
    
    finally:

        if conexao:
            conexao.close()

if __name__ == "__main__":
    
    main()
