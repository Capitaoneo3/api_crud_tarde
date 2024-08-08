from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from app import connect_to_database

usuarios_bp = Blueprint('usuarios', __name__)

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