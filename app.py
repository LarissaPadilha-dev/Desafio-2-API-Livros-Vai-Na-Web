from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
     with sqlite3.connect('database.db') as conn:
          conn.execute("""CREATE TABLE IF NOT EXISTS livros(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     titulo TEXT NOT NULL,
                     categoria TEXT NOT NULL,
                     autor TEXT NOT NULL,
                     imagem_url TEXT NOT NULL
                     )""")
          print("Banco de dados inicializado com sucesso! ✅")
init_db()

@app.route('/')
def home_page():
     return'<h2>Minha página inicial</h2>'

@app.route('/doar', methods=['POST'])
def doar():
     dados = request.get_json()
     
     titulo = dados.get('titulo')
     categoria = dados.get('categoria')
     autor = dados.get('autor')
     imagem_url = dados.get('imagem_url')
     
     if not all([titulo, categoria, autor, imagem_url]):
         return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

     with sqlite3.connect('database.db') as conn:
          conn.execute("""INSERT INTO livros (titulo, categoria, autor, imagem_url)
                     VALUES (?,?,?,?) 
                     """, (titulo, categoria, autor, imagem_url))
          conn.commit()
           
          return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201

if __name__ == '__main__':
     app.run(debug=True)