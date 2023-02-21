
import traceback

from config import Connection, connect

from query_tables import create_tables

from container import container

from adapters.inbound.menu_adapter import menu

from adapters.outbound.repositories.repository import repository


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
