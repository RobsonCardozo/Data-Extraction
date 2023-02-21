from flask import Flask, render_template, request
from pymongo import MongoClient

# Configurações do Flask
app = Flask(__name__, template_folder='../templates/')
app.config['DEBUG'] = True

# Configurações do MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['wikipedia']
collection = db['baseconhecimento']

# Rota principal do Flask
@app.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        # Obtém os dados digitados pelo usuário
        name = request.form['name']
        age = request.form['age']

        # Salva os dados no MongoDB
        collection.insert_one({'name': name, 'age': age})

        return render_template('success.html')
    else:
        return render_template('formulario.html')

if __name__ == '__main__':
    app.run()
