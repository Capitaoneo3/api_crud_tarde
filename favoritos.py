from flask import Blueprint, request, jsonify
import mysql.connector
from utils import connect_to_database  # Importação da função de conexão

favoritos_bp = Blueprint('favoritos', __name__)

# Rota para listar todos os posts favoritos de um usuário
@favoritos_bp.route('/usuarios/<int:usuario_id>/favoritos', methods=['GET'])
def get_posts_favoritos(usuario_id):
    connection = connect_to_database()
    if not connection:
        return jsonify({"message": "Erro interno do servidor ao conectar ao banco de dados"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT p.id, p.titulo, p.conteudo, p.autor_id, p.data_publicacao FROM posts p "
                       "JOIN posts_favoritos pf ON p.id = pf.post_id "
                       "WHERE pf.usuario_id = %s", (usuario_id,))
        posts_favoritos = cursor.fetchall()
        return jsonify(posts_favoritos)
    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao buscar os posts favoritos", "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# Rota para adicionar um post aos favoritos de um usuário
@favoritos_bp.route('/usuarios/<int:usuario_id>/favoritos', methods=['POST'])
def add_post_favorito(usuario_id):
    data = request.get_json()
    post_id = data.get('post_id')

    if not post_id:
        return jsonify({"message": "Por favor, forneça o ID do post para adicionar aos favoritos"}), 400

    connection = connect_to_database()
    if not connection:
        return jsonify({"message": "Erro interno do servidor ao conectar ao banco de dados"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO posts_favoritos (usuario_id, post_id) VALUES (%s, %s)", (usuario_id, post_id))
        connection.commit()
        return jsonify({"message": "Post adicionado aos favoritos com sucesso"}), 201
    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao adicionar o post aos favoritos", "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# Rota para remover um post dos favoritos de um usuário
@favoritos_bp.route('/usuarios/<int:usuario_id>/favoritos/<int:post_id>', methods=['DELETE'])
def remove_post_favorito(usuario_id, post_id):
    connection = connect_to_database()
    if not connection:
        return jsonify({"message": "Erro interno do servidor ao conectar ao banco de dados"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM posts_favoritos WHERE usuario_id = %s AND post_id = %s", (usuario_id, post_id))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Post não encontrado nos favoritos do usuário"}), 404
        return jsonify({"message": "Post removido dos favoritos com sucesso"})
    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao remover o post dos favoritos", "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
