import re
from dataclasses import dataclass
from typing import Callable, Dict, TypedDict
from config import system, name, Connection, connect, Cursor


def clear_screen():

    system('cls') if name.lower() == 'nt' else system('clear')


def conta_cliente(conta: str):
    return "SELECT CONTA FROM DADOS_BANCARIOS WHERE CONTA =:CONTA", (conta,)


def consultar_saldo_conta_usuario(cursor, conta_usuario):
    querry = "SELECT Saldo FROM Dados_Bancarios WHERE Conta =:conta_usuario"
    saldo_usuario = cursor.execute(querry, (conta_usuario,)).fetchone()[0]
    return saldo_usuario


def consultar_saldo_conta_final(cursor, conta_usuario_final):
    querry = "SELECT Saldo FROM Dados_Bancarios WHERE Conta =:conta_usuario_final"
    saldo_usuario_final = cursor.execute(
        querry, (conta_usuario_final,)).fetchone()[0]
    return saldo_usuario_final


def saque(cursor, conta_usuario, saldo_usuario):
    valor_do_saque = int(input("Digite o valor do saque: "))

    if saldo_usuario >= valor_do_saque:

        valor_debitado = saldo_usuario - valor_do_saque
        querry = "UPDATE Dados_Bancarios SET Saldo =:valor_debitado WHERE Conta =:conta_usuario"
        cursor.execute(querry, (valor_debitado, conta_usuario,))

        print("Saque efetuado com sucesso!")

        clear_screen()

    else:
        print("Saldo insuficiente!")


def consultar_saldo(saldo_usuario):
    print(f"Seu saldo atual é de {saldo_usuario} reais!")


def deposito(cursor, conta_usuario, saldo_usuario):
    valor_deposito = int(input("Digite o valor do depósito: "))

    valor_acrescido = saldo_usuario + valor_deposito
    querry = "UPDATE Dados_Bancarios SET Saldo =:valor_acrescido WHERE Conta =:conta_usuario"
    cursor.execute(querry, (valor_acrescido, conta_usuario))

    print("Deposito efetuado com sucesso!")


def opcoes_finais():

    print("\nDigite 0 para voltar ao menu incial e 5 para sair!")
    opcao = int(input("Digite sua opção: "))

    if opcao == 5:
        opcao = 5
    elif opcao == 0:
        opcao = 0
    else:
        "Opção invalida"

    return opcao


@dataclass(frozen=False)
class CustomerDTO():
    name: str
    account: str
    balance: str

# class CustomerDictionary(TypedDict):
#     nome: str
#     conta: str
#     saldo: str


def check_fields(customer: dict) -> bool:

    clear_screen()

    print("\n>>> Verificando formulário ... <<<")

    fail = False

    pattern_name = r'^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$'

    pattern_account = r'\d{5}-\d{1}$'

    def isFloat(value):
        try:
            return True if float(value) else False
        except:
            return False

    if len(customer["name"]) < 10:

        fail = True if len(name :=
                           input('\nNome deve possuir no mínimo 10 caracteres: ')
                           .strip()) < 10 else False

        customer.update({"name": name})

    elif re.match(pattern_name, customer["name"]) is None:

        fail = True if re.match(pattern_name,
                                name := input('\nNome deve possuir apenas caracteres válidos: ')
                                .strip()) is None else False

        customer.update({"name": name})

    if re.match(pattern_account, customer["account"]) is None:

        fail = True if re.match(pattern_account,
                                account := input('\nConta deve obedecer o formato 00000-0: ')
                                .strip()) is None else False

        customer.update({"account": account})

    if isFloat(customer["balance"]) is False:

        fail = False if isFloat(balance := input('\nInforme um valor decimal para saldo: ')
                                .strip()) else True

        customer.update({"balance": balance})

    return fail


def main_menu(account_generator: Callable[[], tuple],
              get_account: Callable[[tuple], tuple],
              create_new_account: Callable[[tuple], tuple]) -> dict | None:

    customer = {}

    script = "\nSEJA BEM VINDO AO TERMINAL ATM - STARS***\
          \n\n\
          1 > Acessar conta\n\
          2 + Cadastrar conta\n\
          3 - Sair"

    print(script)

    while True:

        match input("\nSelecione uma opção:_").strip():

            case "1":

                clear_screen()

                primary_account: str | None = None

                message = "\nInforme uma conta válida:_"

                for i in range(3):

                    primary_account = input(message).strip()

                    if len(primary_account) < 7:

                        message = "\nInforme uma conta válida para pesquisa:_"

                    else:

                        account = get_account((primary_account,))

                        if account is None:
                            message = "\nConta não localizada! Digite novamente:_"

                        if i >= 2:
                            raise Exception(
                                "Favor entrar em contato com sua agência!")

                if primary_account is None:
                    input(
                        "\n!!!Conta não identificada, acione qualquer tecla para retornar ao menu:_")
                    break

                # name = ""
                # account = ""

                # customer = {'name': name,
                #             'account': account}
            case "2":

                clear_screen()

                print("\nIniciando cadastro de conta...")

                accounts = account_generator()

                for account in accounts:
                    print(f"{str(*account.keys())} - {str(*account.values())}")

                num_account = input(
                    'Selecione uma das contas geradas:_').strip()

                name = input('Informe um nome para cliente:_').strip()

                balance = input('Informe um valor:_').strip()

                while True:

                    create, occurrences, account = create_new_account(
                        (num_account, name, balance, accounts))

                    if create is False:

                        if occurrences.get("account_num") is not None:
                            num_account = input(
                                f'{occurrences["account_num"]}:_').strip()

                        elif occurrences.get("name") is not None:
                            name = input(f'{occurrences["name"]}:_').strip()

                        elif occurrences.get("balance") is not None:
                            balance = input(
                                f'{occurrences["balance"]}:_').strip()

                    else:
                        # clear_screen()

                        input(
                            f"\nConta {account} cadastrada com sucesso!!!\nPressione qualquer tecla para retornar ao menu...")

                        # clear_screen()

                        print(script)

                        break
                break

            case "3":
                break

        break

    return customer if customer else None


def menu(account_generator_inside_port: Callable[[], tuple],
         create_new_customer_inside_port: Callable[[tuple], tuple],
         get_account_inside_port: Callable[[tuple], tuple],
         execute_transfer_inside_port: Callable[[str, str, float], str]) -> None:

    clear_screen()

    main_menu(account_generator_inside_port,
              get_account_inside_port,
              create_new_customer_inside_port)

    return

    primary_account: str | None = None

    total_attempts = 0

    clear_screen()

    roteiro = """
    
    SEJA BEM VINDO AO TERMINAL ATM - STARS***
    ....selecione uma opção

    1 - Informe sua conta  
    2 - Realizar transferência
    3 - Realizar saque
    4 - Consultar saldo
    5 - Realizar depósito
    6 - Cadastrar uma conta
    7 - Sair

    """

    print(roteiro)

    while True:

        match input("\nDigite uma opção:").strip():

            case "1":

                message = "\nInforme uma conta válida: "

                for i in range(3):

                    primary_account = input(message).strip()

                    if len(primary_account) < 7:

                        message = "\nConta necessária para pesquisa: "

                    else:

                        account = get_account_inside_port((primary_account,))

                        if account is None:
                            message = "\nConta não localizada! Digite novamente: "

                        if i >= 2:
                            raise Exception(
                                "Favor entrar em contato com sua agência!")

            case "2":

                if primary_account:

                    secondary_account = input(
                        "Digite a conta de destino: ").strip()

                    valor_transferencia = input(
                        "Digite o valor que seja transferir: ").strip()

                    customer = execute_transfer_inside_port(primary_account,
                                                            secondary_account,
                                                            float(valor_transferencia))

                    print(customer)

                else:
                    print("Informe sua conta para transferência")

            case "3":

                clear_screen()

                # saque(cursor,
                #       primary_account,
                #       consultar_saldo_conta_usuario(cursor, primary_account))

                # option = opcoes_finais()

                pass

            case "4":

                # limpar_tela()
                # consultar_saldo(consultar_saldo_conta_usuario(cursor, primary_account))
                # option = opcoes_finais()
                pass

            case "5":

                # limpar_tela()
                # deposito(cursor, primary_account, consultar_saldo_conta_usuario(cursor, primary_account))
                # option = opcoes_finais()
                pass

            case "6":

                clear_screen()

                print("\nIniciando cadastro de conta...")

                customer = {'name':
                            input('\nInforme um nome: ').strip(),
                            'account':
                            input('\nInforme uma conta no modelo 00000-0: ').strip(),
                            'balance':
                            input('\nInforme um saldo: ').strip()}

                while True:

                    if check_fields(customer) is True:

                        clear_screen()

                        if input("\n>>> Foram identificadas ocorrências no cadastro de conta! <<<\
                                 \nTecle ENTER para continuar ou [C] para cancelar e retornar o menu: ").upper() == "C":

                            clear_screen()

                            print(roteiro)

                            break

                    else:

                        create_new_customer_inside_port((customer['name'],
                                                         customer['account'],
                                                         customer['balance']))

                        clear_screen()

                        input(
                            f"\nConta {customer['account']} cadastrada com sucesso!!!\nPressione qualquer tecla para retornar ao menu...")

                        clear_screen()

                        print(roteiro)

                        break

            case "7":

                message = "Confirme sim(Y) para sair..."

                for i in range(3):
                    if input(message)\
                            .strip().upper() in ("Y", "YES", "S", "SIM", "OK", "N", "NO", "NOT"):
                        return
                    else:
                        message = "Opção inválida, informe sim(Y) para sair ou não(N) para cancelar..."

                    if i >= 2:
                        print(
                            "\n>> Você atingiu um número máximo de tentativas, selecione uma opção de menu...\n")

            case _:

                if total_attempts >= 2:
                    raise Exception(
                        "Você excedeu um número total de tentativas")

                else:

                    print("Opção de menu inválida")

                    total_attempts += 1
