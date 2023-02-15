from typing import Callable, Dict, TypedDict
from config import system, name, Connection, connect, Cursor


def limpar_tela():

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

        limpar_tela()

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

from dataclasses import dataclass


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

import re

@dataclass(frozen=False)
class CustomerDTO():
    name: str
    account: str
    balance: str

class CustomerDictionary(TypedDict):
    nome: str
    conta: str
    saldo: str

def check_fields(customer: CustomerDTO) -> tuple[bool, CustomerDTO]:

    fail = False

    def isFloat(value):
        try:
            return True if float(value) else False
        except:
            return False

    if len(customer.name) < 10:
        customer.name = input(
            '\nNome deve possuir no mínimo 10 caracteres: ').strip()
        fail = True

    elif re.match(r'^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$', customer.name) is None:
        customer.name = input(
            '\nNome deve possuir apenas caracteres válidos: ').strip()
        fail = True

    if re.match(r'\d{5}-\d{1}$', customer.account) is None:
        customer.account = input(
            '\nConta deve obedecer o formato 00000-0: ').strip()
        fail = True

    if isFloat(customer.balance) is False:
        customer.balance = input("Informe um valor decimal para saldo: ").strip()
        fail = True

    return fail, customer


# Executando ATM


def menu(get_account_user_case: Callable[[str], str],
         execute_transfer_use_case: Callable[[str, str, float], str],
         create_customer_user_case: Callable[[tuple], None]):

    primary_account: str | None = None

    total_attempts = 0

    limpar_tela()

    print("""
    
    SEJA BEM VINDO AO TERMINAL ATM - STARS***
    ....selecione uma opção

    1 - Informe sua conta  
    2 - Realizar transferência
    3 - Realizar saque
    4 - Consultar saldo
    5 - Realizar depósito
    6 - Cadastrar uma conta
    7 - Sair

    """)

    while True:

        match input("\nDigite uma opção:").strip():

            case "1":

                message = "Informe uma conta válida: "

                for i in range(3):

                    primary_account = input(message).strip()

                    primary_account = get_account_user_case(primary_account)

                    if primary_account is None:

                        message = "Conta não localizada! Digite novamente: "

                    if i >= 2:
                        raise Exception(
                            "Favor entrar em contato com sua agência!")

            case "2":

                if primary_account:

                    secondary_account = input(
                        "Digite a conta de destino: ").strip()

                    valor_transferencia = input(
                        "Digite o valor que seja transferir: ").strip()

                    response = execute_transfer_use_case(primary_account,
                                                         secondary_account,
                                                         float(valor_transferencia))

                    print(response)

                else:
                    print("Informe sua conta para transferência")

            case "3":

                limpar_tela()

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

                customer = CustomerDTO(input('\nInforme um nome: ').strip(),
                                       input(
                                           '\nInforme uma conta no modelo 00000-0: ').strip(),
                                       input('\nInforme um saldo: ').strip())

                while True:
                    
                    fail, customer = check_fields(customer)

                    if fail:
                        print(
                            "\n>>> Ocorrências identificadas no cadastro de conta! <<<")
                    else:
                        create_customer_user_case(
                            (customer.name, customer.account, customer.balance))

                        print(
                            f"\nConta {customer.account} cadastrada com sucesso !!!")

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
