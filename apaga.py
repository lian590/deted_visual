import mysql.connector

# --- Configurações do Banco de Dados (certifique-se de que estão corretas) ---
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "11010412@Pao"
DB_NAME = "star_gate"
TABELA_ROSTOS = "funcionarios"

def conectar_banco():
    """Conecta ao banco de dados MySQL."""
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        return None

def apagar_pessoa_por_nome(nome_pessoa):
    """Apaga um registro da tabela pelo nome da pessoa."""
    mydb = conectar_banco()
    if not mydb:
        return

    mycursor = mydb.cursor()
    query = f"DELETE FROM {TABELA_ROSTOS} WHERE nome = %s"
    values = (nome_pessoa,)

    try:
        mycursor.execute(query, values)
        mydb.commit()
        print(f"{mycursor.rowcount} registro(s) apagado(s) com o nome: {nome_pessoa}")
    except mysql.connector.Error as err:
        print(f"Erro ao apagar registro: {err}")
        mydb.rollback()
    finally:
        mycursor.close()
        mydb.close()

def apagar_pessoa_por_id(pessoa_id):
    """Apaga um registro da tabela pelo ID."""
    mydb = conectar_banco()
    if not mydb:
        return

    mycursor = mydb.cursor()
    query = f"DELETE FROM {TABELA_ROSTOS} WHERE id = %s"
    values = (pessoa_id,)

    try:
        mycursor.execute(query, values)
        mydb.commit()
        print(f"{mycursor.rowcount} registro(s) apagado(s) com o ID: {pessoa_id}")
    except mysql.connector.Error as err:
        print(f"Erro ao apagar registro: {err}")
        mydb.rollback()
    finally:
        mycursor.close()
        mydb.close()

if __name__ == "__main__":
    while True:
        print("\nEscolha uma opção para apagar um registro:")
        print("1 - Apagar por nome")
        print("2 - Apagar por ID")
        print("3 - Sair")
        opcao = input("Digite sua escolha: ")

        if opcao == '1':
            nome_para_apagar = input("Digite o nome da pessoa a ser apagada: ").strip()
            apagar_pessoa_por_nome(nome_para_apagar)
        elif opcao == '2':
            try:
                id_para_apagar = int(input("Digite o ID da pessoa a ser apagada: "))
                apagar_pessoa_por_id(id_para_apagar)
            except ValueError:
                print("ID inválido. Por favor, digite um número inteiro.")
        elif opcao == '3':
            print("Saindo.")
            break
        else:
            print("Opção inválida. Tente novamente.")
       