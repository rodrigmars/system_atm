
import traceback

from config import Connection, connect

from container import container

from adapters.inbound.menu_adapter import menu

from adapters.outbound.repositories.repository import repository

def create_tables() -> str:
    # DROP TABLE IF EXISTS DADOS_BANCARIOS;
    return """
    BEGIN;

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

        conexao = connect("atm_stars.db")

        cursor = conexao.cursor()

        cursor.executescript(create_tables())

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
