from flask import Flask
from usuarios import usuarios_bp
from posts import posts_bp
from favoritos import favoritos_bp
from flask_cors import CORS
import os
import mysql.connector
app = Flask(__name__)
CORS(app)  # Isso permitirá que todas as origens façam requisições para a API
app.config['SECRET_KEY'] = 'your_secret_key_here'


# Configurações do banco de dados
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Função para conectar ao banco de dados
def connect_to_database():
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


# Registrar blueprints
app.register_blueprint(usuarios_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(favoritos_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)