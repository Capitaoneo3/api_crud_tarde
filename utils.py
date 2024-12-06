import mysql.connector


# Função para conectar ao banco de dados
def connect_to_database():
    db_host = 'localhost'
    db_user = 'root'
    db_password = ''
    db_name = 'formulario_db'

    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    
    