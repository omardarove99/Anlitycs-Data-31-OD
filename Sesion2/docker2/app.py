from flask import Flask

app=Flask(__name__)

#Ruta 1 : Retorna un saludo simple
@app.route('/api/hello')
def hello():
    """
    GET /api/hello
    Retorna = "Hola, bienvenido a mi API"    
    """
    return "Hola, bienvenido a mi API"

#Iniciar el servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)