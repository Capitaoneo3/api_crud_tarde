from flask import Blueprint, request, jsonify
import mysql.connector
from utils import connect_to_database  # Importação da função de conexão

posts_bp = Blueprint('posts', __name__)

# Rota para listar todos os posts
@posts_bp.route('/posts', methods=['GET'])
def get_posts():
    connection = connect_to_database()
    if not connection:
        return jsonify({"message": "Erro interno do servidor ao conectar ao banco de dados"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, titulo, conteudo, autor_id, data_publicacao FROM posts")
        posts = cursor.fetchall()
        return jsonify(posts)
    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao buscar os posts", "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# Rota para buscar um post específico pelo ID
@posts_bp.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    connection = connect_to_database()
    if not connection:
        return jsonify({"message": "Erro interno do servidor ao conectar ao banco de dados"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, titulo, conteudo, autor_id, data_publicacao FROM posts WHERE id = %s", (id,))
        post = cursor.fetchone()
        if not post:
            return jsonify({"message": "Post não encontrado"}), 404
        return jsonify(post)
    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao buscar o post", "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# Rota para criar um novo post
@posts_bp.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    titulo = data.get('titulo')
    conteudo = data.get('conteudo')
    autor_id = data.get('autor_id')

    if not titulo or not conteudo or not autor_id:
        return jsonify({"message": "Por favor, forneça título, conteúdo e ID do autor"}), 400

    connection = connect_to_database()
    if not connection:
        return jsonify({"message": "Erro interno do servidor ao conectar ao banco de dados"}), 500

    try:
        cursor = connection.cursor()
        sql = "INSERT INTO posts (titulo, conteudo, autor_id) VALUES (%s, %s, %s)"
        cursor.execute(sql, (titulo, conteudo, autor_id))
        connection.commit()
        return jsonify({"message": "Post criado com sucesso"}), 201
    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao criar o post", "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# Rota para atualizar um post pelo ID
@posts_bp.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()
    titulo = data.get('titulo')
    conteudo = data.get('conteudo')

    if not titulo and not conteudo:
        return jsonify({"message": "Por favor, forneça pelo menos o título ou conteúdo para atualizar"}), 400

    connection = connect_to_database()
    if not connection:
        return jsonify({"message": "Erro interno do servidor ao conectar ao banco de dados"}), 500

    try:
        cursor = connection.cursor()
        sql = "UPDATE posts SET titulo = %s, conteudo = %s WHERE id = %s"
        cursor.execute(sql, (titulo, conteudo, id))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Post não encontrado"}), 404
        return jsonify({"message": "Post atualizado com sucesso"})
    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao atualizar o post", "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# Rota para deletar um post pelo ID
@posts_bp.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    connection = connect_to_database()
    if not connection:
        return jsonify({"message": "Erro interno do servidor ao conectar ao banco de dados"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Post não encontrado"}), 404
        return jsonify({"message": "Post deletado com sucesso"})
    except mysql.connector.Error as e:
        return jsonify({"message": "Erro ao deletar o post", "error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
