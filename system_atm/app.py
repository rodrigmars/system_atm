
import traceback

from config import Connection, connect

from container import container

from adapters.inbound.menu_adapter import menu

from adapters.outbound.repositories.repository import repository

def create_tables() -> str:
    # DROP TABLE IF EXISTS BANK_DATA;
    # DROP INDEX IF EXISTS INDEX_ACCOUNT;
    return """
    BEGIN;

    CREATE TABLE IF NOT EXISTS BANK_DATA (
        ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        NAME TEXT NOT NULL,
        ACCOUNT TEXT NOT NULL UNIQUE,
        BALANCE NUMERIC NOT NULL,
        TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE UNIQUE INDEX IF NOT EXISTS INDEX_ACCOUNT ON BANK_DATA (ACCOUNT);

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
