import sqlite3
import os

conexao = sqlite3.connect("Dados.db")
cursor = conexao.cursor()

def limpar_tela():
    os.system("cls")

def conta_cliente():

#    try:
        conta = int(input("Digite sua conta: "))
        querry = "SELECT Conta FROM Dados_Bancarios WHERE Conta =:conta"
        resultado = cursor.execute(querry, (conta, )).fetchone()
        return resultado 
        
#    except: 
#        limpar_tela()
#        print("Conta invalida ou formato inválido, digite novmente!")
#        conta_cliente()
    
def consultar_saldo(conta_cliente):
    
    try:
        querry = "SELECT Saldo FROM Dados_Bancarios WHERE Conta =:conta_cliente"
        saldo = cursor.execute(querry, (conta_cliente, )).fetchone()[0]
        print(saldo)
    except Exception as erro:
        print(erro)

consultar_saldo(conta_cliente())