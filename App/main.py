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
    clear()
    print("Conexão estabelecida!")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")

    return connection


# Interface inicial da aplicação
def main_menu():
    print(">>>>>>>>>>> Meu Notebook, Minha Vida <<<<<<<<<<<")
    print("Bem-vindo(a) à Página Inicial do nosso Sistema!", end="\n\n")
    print("Escolha uma opção:")
    print("1. Cadastrar dispositivo")
    print("2. Buscar empréstimos por intervalo de data")
    print("3. Sair")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")


# Aplicação que possui as opções das funcionalidades
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


# Função que realiza o cadastro de dispositivos
# Ela realiza a entrada dos valores para o insert
def cadastro_dispositivo(connection):
    while(True):
        try:
            # Entrada de valores
            print("Essa é a seção de informações.")
            numero_serial = input("Número serial: ")
            tipo = input("Tipo: ")
            modelo = input("Modelo: ")
            empresa = input("Empresa: ")
            clear()

            # Inserção SQL
            sql = """INSERT INTO DISPOSITIVO
                    VALUES (:numero_serial, :tipo, :modelo, 'DISPONIVEL', 0, :empresa)"""
            cursor = connection.cursor()
            cursor.execute(sql, [numero_serial.upper(), tipo.upper(), modelo.upper(), empresa.upper()])

        # Tratamento de exceções do banco
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

            # Caso de erro ele dá rollback e não executa a ação definitivamente
            connection.rollback()

        else:
            # Caso de sucesso de inserção
            print("Dispositivo adicionado com sucesso!")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")

            cursor.close()

            # Caso dê certo ao final da ação ele commita as mudanças
            connection.commit()

        finally:
            # Final de cada ação que permite a repetição da funcionalidade ou saída dela
            acao = input("Você ainda deseja inserir um dispositivo? Se sim, digite 'S': ")
            clear()

            if acao.upper() != 'S':
                cursor.close()
                return



# Função que realiza a busca de empréstimos de dispositivos baseados no intervalo de datas
# Ela realiza a entrada dos valores para o select
def select_emprestimo(connection):
    while(True):
        try:
            print("Essa é a seção de ação.")
            print("Utilize o formato (DD-MM-YYYY ou DD/MM/YYYY)")
            data_inicio = input("Data de início: ")
            data_fim = input("Data de fim: ")
            clear()
            
            sql = """SELECT E.DATA, E.DATA_DEVOLUCAO, D.NUMERO_SERIAL, D.TIPO, D.MODELO, D.STATUS, A.NOME, A.REG_ALUNO, ESC.NOME FROM DISPOSITIVO D 
                    JOIN EMPRESTIMO E ON D.NUMERO_SERIAL = E.DISPOSITIVO 
                    JOIN ALUNO A ON E.ALUNO = A.CPF
                    JOIN ESCOLA_PARCEIRA ESC ON A.ESCOLA = ESC.CODIGO_INEP
                    WHERE E.DATA BETWEEN TO_DATE(:data_inicio, 'DD-MM-YYYY') AND TO_DATE(:data_fim, 'DD-MM-YYYY')
                    ORDER BY E.DATA DESC"""
            
            cursor = connection.cursor()
            cursor.execute(sql,[data_inicio, data_fim])
        
        # Tratamento de exceções
        except oracledb.Error as e:
            error_obj, = e.args

            if(error_obj.code == 1858):
                print("Digite um valor numérico válido de data")
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")
            elif (error_obj.code == 1861):
                print("Use a formatação necessária na entrada")
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")
            else:
                print("Error Message:", error_obj.message)
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")

            # Caso de erro ele dá rollback e não executa a ação definitivamente
            connection.rollback()

        else:
            # Caso em que a busca é bem sucedida
            tabela = cursor.fetchall()
            print("------------------------------------------------------------------", end="\n")
            print(f"EMPRESTIMOS REALIZADOS ENTRE {data_inicio} E {data_fim}", end="\n")
            print("------------------------------------------------------------------", end="\n")
            if tabela == []:
                print("\nNão foi encontrado nenhum empréstimo nesse intervalo de tempo.\n")
            else:
                for tupla in tabela:
                    print("Data de retirada:", tupla[0].strftime("%d-%m-%Y"))
                    print("Data de devolução:", tupla[1].strftime("%d-%m-%Y"))
                    print("Número serial:", tupla[2])
                    print("Tipo:", tupla[3])
                    print("Modelo:", tupla[4])
                    print("Status:", tupla[5])
                    print("\nNome do Aluno:", tupla[6])
                    print("RA:", tupla[7])
                    print("Escola:", tupla[8])
                    print("------------------------------------------------------------------", end="\n")
                    
            print("\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", end="\n\n")

            # Caso dê certo ao final da ação ele commita as mudanças
            connection.commit()

        finally:
            # Final de cada ação que permite a repetição da funcionalidade ou saída dela
            acao = input("Você ainda deseja buscar empréstimos? Se sim, digite 'S': ")
            clear()

            if acao.upper() != 'S':
                cursor.close()
                return


# Funçãoq que limpa o terminal
def clear(): 
    if name == 'nt': 
        x = system('cls') 
    else: 
        x = system('clear') 


# Função main em que o código será executado
if __name__ == "__main__":
    clear()
    try:
        
        # Tentando conexão
        connection = connect()
        if(not connection):
            exit()

        # Aplicação rodando
        while(True):
            application(connection)
        
        # Fim da conexão
        connection.close()

    # Tratamento de caso ^C seja acionado
    except KeyboardInterrupt:
        print("\nEncerrando a aplicação")
        # Fim da conexão
        connection.close()
        exit()
