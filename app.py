from flask import Flask, request, jsonify
import mariadb
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Isso permitirá que todas as origens façam requisições para a API
app.config['SECRET_KEY'] = 'your_secret_key_here'


# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'formulario_db'

@app.route('/register', methods=['POST'])
def register():
    # Conexão com o banco de dados
    try:
        connection = mariadb.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    except mariadb.Error as e:
        return jsonify({"message": "Erro ao conectar com o banco de dados", "error": str(e)}), 500

    try:
        cursor = connection.cursor()

        data = request.get_json()
        nome = data.get('nome')
        senha  = data.get('senha')
        cpf = data.get('cpf')

        # Verificar se o usuário já existe
        try:
            cursor.execute('SELECT * FROM usuarios WHERE nome = ?', (nome,))
            usuario_existente = cursor.fetchone()
        except mariadb.Error as e:
            return jsonify({"message": "Erro ao verificar existência de usuário", "error": str(e)}), 500

        if usuario_existente:
            return jsonify({"message": "Usuário já existe"}), 409

        # Gerar hash da senha
        hashed_password = generate_password_hash(senha, method='pbkdf2:sha256:600000')

        # Inserir novo usuário no banco de dados
        try:
            sql = "INSERT INTO usuarios (nome, cpf, senha) VALUES (?, ?, ?)"
            cursor.execute(sql, (nome, cpf, hashed_password,))
            connection.commit()
        except mariadb.Error as e:
            return jsonify({"message": "Erro ao registrar usuário", "error": str(e)}), 500

        return jsonify({"message": "Usuário registrado com sucesso"}), 201

    except Exception as e:
        return jsonify({"message": "Erro ao processar a solicitação", "error": str(e)}), 500

    finally:
        # Fechar o cursor e a conexão com o banco de dados
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nome = data.get('nome')
    senha = data.get('senha')

    # Conexão com o banco de dados
    try:
        connection = mariadb.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    except mariadb.Error as e:
        return jsonify({"message": "Erro ao conectar com o banco de dados", "error": str(e)}), 500

    try:
        cursor = connection.cursor()

        # Buscar todos os usuários
        try:
            cursor.execute('SELECT * FROM usuarios')
            usuarios = cursor.fetchall()
        except mariadb.Error as e:
            return jsonify({"message": "Erro ao executar consulta no banco de dados", "error": str(e)}), 500

        usuario_descoberto = None
        for usuario in usuarios:
            if usuario[1] == nome:
                usuario_descoberto = usuario
                break

        # Verificar usuário e senha
        if not usuario_descoberto or not check_password_hash(usuario_descoberto[3], senha):
            return jsonify({"message": "Nome de usuário ou senha inválidos"}), 401

        return jsonify({"message": "Login bem-sucedido"}), 200

    except Exception as e:
        return jsonify({"message": "Erro ao processar a solicitação", "error": str(e)}), 500

    finally:
        # Certificar-se de que a conexão com o banco de dados é fechada
        if 'connection' in locals():
            connection.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

