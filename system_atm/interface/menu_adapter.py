from config import system, name, Connection, connect, Cursor

def limpar_tela():

    system('cls') if name.lower() == 'nt' else system('clear')


def conta_final(cursor: Cursor):

    conta_usuario_final = int(input("Digite a conta de destino: "))

    querry = "SELECT Conta FROM Dados_Bancarios WHERE Conta =:conta_usuario_final"

    resultado = cursor.execute(querry, (conta_usuario_final,)).fetchone()[0]
    
    if resultado != "":
        return conta_usuario_final
        
    # except:
    #     limpar_tela()
    #     print("Conta não encontrada ou formato inválido! Digite novamente.")
    #     conta_final()


def conta_cliente(conta: str):
    return "SELECT CONTA FROM DADOS_BANCARIOS WHERE CONTA =:CONTA", (conta,)

def consultar_saldo_conta_usuario(cursor, conta_usuario):
    querry =  "SELECT Saldo FROM Dados_Bancarios WHERE Conta =:conta_usuario"
    saldo_usuario = cursor.execute(querry, (conta_usuario,)).fetchone()[0]
    return saldo_usuario

def consultar_saldo_conta_final(cursor, conta_usuario_final):
    querry =  "SELECT Saldo FROM Dados_Bancarios WHERE Conta =:conta_usuario_final"
    saldo_usuario_final = cursor.execute(querry, (conta_usuario_final,)).fetchone()[0]
    return saldo_usuario_final

def transferencia(cursor, saldo_usuario, conta_usuario, saldo_usuario_final, conta_usuario_final):
    
    valor_da_transferencia = int(input("Digite o valor que seja transferir: "))

    if saldo_usuario >= valor_da_transferencia:
        
        valor_debitado = saldo_usuario - valor_da_transferencia
        querry_debitar = "UPDATE Dados_Bancarios SET Saldo =:valor_debitado WHERE Conta =:conta_usuario"
        cursor.execute(querry_debitar, (valor_debitado, conta_usuario,))
        
        valor_acrescido = saldo_usuario_final + valor_da_transferencia
        querry_acrescentar = "UPDATE Dados_Bancarios SET Saldo =:valor_acrescido WHERE Conta =:conta_usuario_final"
        cursor.execute(querry_acrescentar, (valor_acrescido, conta_usuario_final,))
        
        print("Transferência executada com sucesso!")
        
    else:
        print("Saldo insuficiente!")
        
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

def deposito (cursor, conta_usuario, saldo_usuario):
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

# Executando ATM

def menu(cursor:Cursor):

    bank_account: str | None = None
    
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
    6 - Sair

    """)
                    
    while True:
    
        match input("Digite uma opção:").strip():

            case "1":

                message = "Informe uma conta válida: "

                for _ in range(3):
                    
                    bank_account = cursor.execute(*conta_cliente(input(message).strip())).fetchone()

                    if bank_account is None:

                        message = "Conta não localizada! Digite novamente: "

                if bank_account is None:
                    raise Exception("Favor entrar em contato com sua agência!")

            case "2": 

                conta_destino = conta_final(cursor)

                transferencia(cursor, 
                            consultar_saldo_conta_usuario(cursor, bank_account), 
                            bank_account, consultar_saldo_conta_final(cursor, conta_destino), 
                            conta_destino)
                
                option = opcoes_finais()
                
            case "3":
                
                limpar_tela()
                
                saque(cursor, 
                      bank_account, 
                      consultar_saldo_conta_usuario(cursor, bank_account))
                
                option = opcoes_finais()

            case "4":
                
                limpar_tela()
                consultar_saldo(consultar_saldo_conta_usuario(cursor, bank_account))
                option = opcoes_finais()

            case "5":
                
                limpar_tela()
                deposito(cursor, bank_account, consultar_saldo_conta_usuario(cursor, bank_account))
                option = opcoes_finais()

            case "6":

                message = "Confirme sim(Y) para sair..."

                for _ in range(3):
                    if input(message)\
                            .strip().upper() in ("Y", "YES", "S", "SIM", "OK", "N", "NO", "NOT"):
                        break
                    else:
                        message = "Opção inválida, informe sim(Y) para sair ou não(N) para cancelar..."

            case _:

                if total_attempts >= 2:                    
                    raise Exception("Você excedeu um número total de tentativas")
                
                else:

                    print("Opção de menu inválida")

                    total_attempts += 1
