from flask import Flask
from usuarios import usuarios_bp
from posts import posts_bp
from favoritos import favoritos_bp
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Permite todas as origens fazerem requisições para a API
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Registrar blueprints
app.register_blueprint(usuarios_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(favoritos_bp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)