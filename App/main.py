# Inserção de Dispositivo.
# busca de empréstimos dado uma data.


from os import system, name
import os    

# instalar biblioteca oracledb]
import oracledb

# instalar biblioteca dotenv
import dotenv

def connect():
    # Busca das informações
    dotenv.load_dotenv(dotenv.find_dotenv())
    USERNAME = os.getenv("USER_NAME")
    USER_PASSWORD = os.getenv("USER_PASSWORD")

    # Tentativa de conexão
    print("Tentando conexão...")
    connection = oracledb.connect(user=USERNAME, password=USER_PASSWORD, host="orclgrad1.icmc.usp.br", port=1521, service_name="pdb_elaine.icmc.usp.br")
    print("Conexão estabelecida!")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")

    return connection

def main_menu():
    print(">>>>>>>> Meu Notebook, Minha Vida <<<<<<<<")
    print("Bem-vindo(a) à Página Inicial do nosso Sistema!")
    print("Escolha uma opção:")
    print("1. Cadastrar dispositivo")
    print("2. Buscar empréstimos por intervalo de data")
    print("3. Sair")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")

    option = input("Digite o número da opção desejada: ")
    clear()

    if option == "1":
        cadastro_dispositivo()
    elif option == "2":
        perform_action()
    elif option == "3":
        connection.close()
        exit()
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")


def cadastro_dispositivo():
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
            else:
                print("Error Message:", error_obj.message)
            
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")
            connection.rollback()

            acao = input("Você ainda deseja inserir um dispositivo? Se sim, digite 'S': ")
            clear()

            # Saida do loop
            if acao.upper() != 'S':
                cursor.close()
                return

        else:
            print ("Dispositivo adicionado com sucesso!")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")
            connection.commit()
            cursor.close()
            return

    # Coloque aqui o código para mostrar as informações desejadas.
    # Você pode adicionar mais opções de menu dentro dessa função, se necessário.
    # Lembre-se de fornecer uma opção para retornar ao menu principal.

def perform_action():
    cursor = connection.cursor()

    while(True):
        try:
            print("Essa é a seção de ação.")
            print("Utilize o formato (YYYY-MM-DD)")
            data_inicio = input("Data de início: ")
            data_fim = input("Data de fim: ")
            clear()

            cursor.execute("SELECT E.DATA, E.DATA_DEVOLUCAO, D.NUMERO_SERIAL, D.TIPO, D.MODELO, D.STATUS FROM DISPOSITIVO D JOIN EMPRESTIMO E ON D.NUMERO_SERIAL = E.DISPOSITIVO WHERE E.DATA BETWEEN TO_DATE(:data_inicio, 'YYYY-MM-DD') AND TO_DATE(:data_fim, 'YYYY-MM-DD') ORDER BY E.DATA DESC",
                           [data_inicio, data_fim])
        
        except oracledb.Error as e:
            error_obj, = e.args

            print("Error Message:", error_obj.message)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")
            connection.rollback()

            acao = input("Você ainda deseja buscar empréstimos? Se sim, digite 'S': ")
            clear()

            # Saida do loop
            if acao.upper() != 'S':
                cursor.close()
                return

        else:
            tabela = cursor.fetchall()
            print(tabela)
            if tabela == []:
                print("Não foi encontrado nenhum empréstimo nesse intervalo de tempo.")
            else:
                for tuplas in tabela:
                    print(tuplas)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")
            connection.commit()
            cursor.close()
            return



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
    clear()
    try:
        if(not connect()):
            exit()

        while(True):
            main_menu()

    except KeyboardInterrupt:
        print("\nEncerrando a aplicação")
        exit()
