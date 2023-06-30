#-------------------------------------------------------------------------------
# Meu Notebook, Minha Vida.
# Disciplina de Bases de Dados (SSC0240).
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Inserção de Dispositivos e busca de empréstimos dado um intervalo.
#-------------------------------------------------------------------------------

from os import system, name
import os    

# Instalar biblioteca oracledb e pythn-dotenv
import oracledb
import dotenv

# Realiza a conexão ao banco de dados (Oracle)
def connect():
    # Busca das informações no .env
    dotenv.load_dotenv(dotenv.find_dotenv())
    USERNAME = os.getenv("USER_NAME")
    USER_PASSWORD = os.getenv("USER_PASSWORD")

    # Tentativa de conexão
    print("Tentando conexão...")
    connection = oracledb.connect(user=USERNAME, password=USER_PASSWORD, host="orclgrad1.icmc.usp.br", port=1521, service_name="pdb_elaine.icmc.usp.br")
    print("Conexão estabelecida!")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")

    return connection



def main_menu():
    print(">>>>>>>>>>> Meu Notebook, Minha Vida <<<<<<<<<<<")
    print("Bem-vindo(a) à Página Inicial do nosso Sistema!", end='\n')
    print("Escolha uma opção:")
    print("1. Cadastrar dispositivo")
    print("2. Buscar empréstimos por intervalo de data")
    print("3. Sair")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")



def application(connection): 
    main_menu()

    option = input("Digite o número da opção desejada: ")
    clear()

    if option == "1":
        cadastro_dispositivo(connection)
    elif option == "2":
        select_emprestimo(connection)
    elif option == "3":
        connection.close()
        exit()
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")



def cadastro_dispositivo(connection):
    while(True):
        try:
            print("Essa é a seção de informações.")
            numero_serial = input("Número serial: ")
            tipo = input("Tipo: ")
            modelo = input("Modelo: ")
            empresa = input("Empresa: ")
            clear()

            # Inserção SQL
            cursor = connection.cursor()
            cursor.execute("""insert into dispositivo
                            values (:numero_serial, :tipo, :modelo, 'DISPONIVEL', 1, :empresa)""",
                            [numero_serial.upper(), tipo.upper(), modelo.upper(), empresa.upper()])

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
            
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")
            connection.rollback()

            acao = input("Você ainda deseja inserir um dispositivo? Se sim, digite 'S': ")
            clear()

            if acao.upper() != 'S':
                cursor.close()
                return

        else:
            print("Dispositivo adicionado com sucesso!")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")

            cursor.close()
            connection.commit()
            return



def select_emprestimo(connection):
    while(True):
        try:
            print("Essa é a seção de ação.")
            print("Utilize o formato (DD-MM-YYYY)")
            data_inicio = input("Data de início: ")
            data_fim = input("Data de fim: ")
            clear()

            cursor = connection.cursor()
            cursor.execute("""select E.DATA, E.DATA_DEVOLUCAO, D.NUMERO_SERIAL, D.TIPO, D.MODELO, D.STATUS
                            from DISPOSITIVO D 
                            join EMPRESTIMO E
                            on D.NUMERO_SERIAL = E.DISPOSITIVO
                            where E.DATA between TO_DATE(:data_inicio, 'DD-MM-YYYY') and TO_DATE(:data_fim, 'DD-MM-YYYY')
                            order by E.DATA desc""",
                            [data_inicio, data_fim])
        
        except oracledb.Error as e:
            error_obj, = e.args

            print("Error Message:", error_obj.message)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")
            connection.rollback()

            acao = input("Você ainda deseja buscar empréstimos? Se sim, digite 'S': ")
            clear()

            if acao.upper() != 'S':
                cursor.close()
                return

        else:
            tabela = cursor.fetchall()
            if tabela == []:
                print("Não foi encontrado nenhum empréstimo nesse intervalo de tempo.")
            else:
                for tupla in tabela:
                    print("------------------------------------------------", end="\n")
                    print("Data de retirada:", tupla[0].strftime("%d-%m-%Y"))
                    print("Data de devolução:", tupla[1].strftime("%d-%m-%Y"))
                    print("Número serial:", tupla[2])
                    print("Tipo:", tupla[3])
                    print("Modelo:", tupla[4])
                    print("Status:", tupla[5])
                    
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")

            cursor.close()
            connection.commit()
            return



def clear(): 
    if name == 'nt': 
        x = system('cls') 
    else: 
        x = system('clear') 



if __name__ == "__main__":
    clear()
    try:
        connection = connect()
        if(not connection):
            exit()

        while(True):
            application(connection)
        
        connection.close()

    except KeyboardInterrupt:
        print("\nEncerrando a aplicação")
        exit()
