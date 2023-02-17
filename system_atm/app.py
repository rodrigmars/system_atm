
import traceback

from config import Connection, connect

from adapters.inbound.menu_adapter import menu

from adapters.outbound.repositories.repository import repository
from adapters.outbound.repositories.customer_adapter_repository import customer_adapter_repository

from application.ports.inside.customer.create_new_customer_inside_port import create_new_customer_inside_port
from application.ports.inside.customer.get_account_inside_port import get_account_inside_port
from application.ports.inside.customer.execute_transfer_inside_port import execute_transfer_inside_port

from application.services.customer.create_new_customer_service import create_new_customer_service
from application.ports.outside.customer.costumer_repository_outside_port import costumer_repository_outside_port


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

        def container(repository: dict) -> tuple:

            return get_account_inside_port(repository), \
                execute_transfer_inside_port(repository), \
                create_new_customer_inside_port(
                    create_new_customer_service(
                        costumer_repository_outside_port(
                            customer_adapter_repository(repository))))

        menu(*container(repository(cursor)))

    except Exception:

        traceback.print_exc()

        if conexao:
            conexao.rollback()

    finally:

        if conexao:
            conexao.close()


if __name__ == "__main__":

    main()
