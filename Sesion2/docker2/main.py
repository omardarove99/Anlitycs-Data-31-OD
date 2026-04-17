from flask import Flask
from flasgger import Swagger

app = Flask(__name__)

app.config['SWAGGER'] = {
    'title': 'Mi API',
    'uiversion': 3
}

swagger = Swagger(app)

@app.route('/')
def home():
    return "API funcionando"

@app.route('/api/hello')
def hello():
    """
    Endpoint de saludo
    ---
    responses:
      200:
        description: Retorna un mensaje de saludo
    """
    return "Hola Mundo desde Docker"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)