from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from utils import connect_to_database  # Importação da função de conexão

usuarios_bp = Blueprint('usuarios', __name__)


@usuarios_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nome = data.get('nome')
    senha = data.get('senha')
    cpf = data.get('cpf')
    email = data.get('email')

    connection = connect_to_database()
    if not connection:
        return jsonify({"message": "Erro interno do servidor ao conectar ao banco de dados"}), 500

    try:
        cursor = connection.cursor()

        # Verificar se o usuário já existe
        cursor.execute('SELECT * FROM usuarios WHERE nome = %s', (nome,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            return jsonify({"message": "Usuário já existe"}), 409

        # Gerar hash da senha
        hashed_password = generate_password_hash(senha, method='pbkdf2:sha256:600000')

        # Inserir novo usuário no banco de dados
        sql = "INSERT INTO usuarios (nome, cpf, senha, email) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nome, cpf, hashed_password, email))
        connection.commit()

        return jsonify({"message": "Usuário registrado com sucesso"}), 201

    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao registrar usuário", "error": str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@usuarios_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nome = data.get('nome')
    senha = data.get('senha')

    connection = connect_to_database()
    if not connection:
        return jsonify({"message": "Erro interno do servidor ao conectar ao banco de dados"}), 500

    try:
        cursor = connection.cursor()

        # Buscar usuário pelo nome
        cursor.execute('SELECT * FROM usuarios WHERE nome = %s', (nome,))
        usuario = cursor.fetchone()

        if not usuario or not check_password_hash(usuario[3], senha):
            return jsonify({"message": "Nome de usuário ou senha inválidos"}), 401

        return jsonify({"message": "Login bem-sucedido"}), 200

    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao executar consulta no banco de dados", "error": str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()




# Rota para listar todos os usuários
@usuarios_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    connection = connect_to_database()
    if not connection:
        return jsonify({"message": "Erro interno do servidor ao conectar ao banco de dados"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, cpf, email FROM usuarios")
        usuarios = cursor.fetchall()
        return jsonify(usuarios)
    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao buscar os usuários", "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# Rota para buscar um usuário específico pelo ID
@usuarios_bp.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    connection = connect_to_database()
    if not connection:
        return jsonify({"message": "Erro interno do servidor ao conectar ao banco de dados"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, cpf, email FROM usuarios WHERE id = %s", (id,))
        usuario = cursor.fetchone()
        if not usuario:
            return jsonify({"message": "Usuário não encontrado"}), 404
        return jsonify(usuario)
    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao buscar o usuário", "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# Rota para atualizar um usuário pelo ID
@usuarios_bp.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    data = request.get_json()
    nome = data.get('nome')
    cpf = data.get('cpf')
    email = data.get('email')

    if not nome and not cpf and not email:
        return jsonify({"message": "Por favor, forneça pelo menos o nome, CPF ou e-mail para atualizar"}), 400

    connection = connect_to_database()
    if not connection:
        return jsonify({"message": "Erro interno do servidor ao conectar ao banco de dados"}), 500

    try:
        cursor = connection.cursor()
        sql = "UPDATE usuarios SET nome = %s, cpf = %s, email = %s WHERE id = %s"
        cursor.execute(sql, (nome, cpf, email, id))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Usuário não encontrado"}), 404
        return jsonify({"message": "Usuário atualizado com sucesso"})
    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao atualizar o usuário", "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# Rota para deletar um usuário pelo ID
@usuarios_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    connection = connect_to_database()
    if not connection:
        return jsonify({"message": "Erro interno do servidor ao conectar ao banco de dados"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Usuário não encontrado"}), 404
        return jsonify({"message": "Usuário deletado com sucesso"})
    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao deletar o usuário", "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()