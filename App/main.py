# Inserção de Dispositivo.
# busca de empréstimos dado uma data.


from os import system, name
import os    

# instalar biblioteca oracledb]
import oracledb

# instalar biblioteca dotenv
import dotenv

# Busca das informações
dotenv.load_dotenv(dotenv.find_dotenv())
USERNAME = os.getenv("USER_NAME")
USER_PASSWORD = os.getenv("USER_PASSWORD")

# Tentativa de conexão
print("Tentando conexão...")
connection = oracledb.connect(user=USERNAME, password=USER_PASSWORD, host="orclgrad1.icmc.usp.br", port=1521, service_name="pdb_elaine.icmc.usp.br")
print("Conexão estabelecida!")
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")

# Tirar as chamadas recursivas
def main_menu():
    print(">>>>>>>> Meu Notebook, Minha Vida <<<<<<<<")
    print("Bem-vindo(a) à Página Inicial do nosso Sistema!")
    print("Escolha uma opção:")
    print("1. Cadastrar dispositivo")
    print("2. Buscar empréstios por intervalo de data")
    print("3. Sair")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")

    option = input("Digite o número da opção desejada: ")

    if option == "1":
        clear()
        cadastro_dispositivo()
    elif option == "2":
        clear()
        perform_action()
    elif option == "3":
        connection.close()
        clear()
        exit()
    else:
        clear()
        print("Opção inválida. Por favor, escolha uma opção válida.")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")


def cadastro_dispositivo():
    clear()
    
    cursor = connection.cursor()

    while(True):
        try:
            print("Essa é a seção de informações.")
            numero_serial = input("Número serial: ")
            tipo = input("Tipo: ")
            modelo = input("Modelo: ")
            empresa = input("Empresa: ")
            clear()

            cursor.execute("insert into dispositivo values (:numero_serial, :tipo, :modelo, 'DISPONIVEL', 1, :empresa)", 
                           [numero_serial, tipo, modelo, empresa])

        except oracledb.Error as e:
            error_obj, = e.args

            if error_obj.code == 12899:
                print("Valor da entrada excede o tamanho máximo.")
            elif error_obj.code == 1400:
                print("O número serial não pode ser nulo.")
            elif error_obj.code == 2291:
                print("Empresa não encontrada.")
            
            #print("Error Code:", error_obj.code)
            #print("Error Context:", error_obj.context)
            #print("Error Full Code:", error_obj.full_code)
            #print("Error Message:", error_obj.message)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")
            connection.rollback()

            acao = input("Você ainda deseja inserir um dispositivo? Se sim, digite 'S': ")
            print("acao:", acao)
            clear()
            if acao.upper() != 'S':
                return



        else:
            print ("Dispositivo adicionado com sucesso!")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")
            connection.commit()
            return

    # Coloque aqui o código para mostrar as informações desejadas.
    # Você pode adicionar mais opções de menu dentro dessa função, se necessário.
    # Lembre-se de fornecer uma opção para retornar ao menu principal.


def perform_action():
    clear()
    print("Essa é a seção de ação.")
    # cursor.execute("""SELECT * FROM JOGADOR""")
    # for fname, lname in cursor:
    #     print("Values:", fname, lname)
    # Coloque aqui o código para realizar a ação desejada.
    # Você pode adicionar mais opções de menu dentro dessa função, se necessário.
    # Lembre-se de fornecer uma opção para retornar ao menu principal.

def clear(): 
    if name == 'nt': 
        x = system('cls') 
    else: 
        x = system('clear') 


if __name__ == "__main__":
    # connection = cx_Oracle.connect(user=USERNAME, password=USER_PASSWORD, dsn="pdb_elaine.icmc.usp.br/Pratica")
    # cursor = connection.cursor()
    clear()
    while(True):
        main_menu()