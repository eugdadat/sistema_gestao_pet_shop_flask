from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import time

app = Flask(__name__)

# Configurações do Banco
DB_HOST = os.getenv("DB_HOST", "mysql-service")
DB_NAME = os.getenv("DB_NAME", "petvida")
DB_USER = os.getenv("DB_USER", "pet_admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "senha123")

def conectar_bd():
    tentativas = 10
    while tentativas > 0:
        try:
            conexao = mysql.connector.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return conexao
        except mysql.connector.Error as e:
            print(f"Erro ao conectar: {e}")
            tentativas -= 1
            time.sleep(3)
    return None

# --- ROTA PRINCIPAL ---
@app.route("/")
def index():
    return render_template("index.html")

# --- CLIENTES ---
@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    conexao = conectar_bd()
    cursor = conexao.cursor(dictionary=True)
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        cursor.execute("INSERT INTO clientes (nome, telefone, email) VALUES (%s, %s, %s)", (nome, telefone, email))
        conexao.commit()
        return redirect(url_for("clientes"))
    
    cursor.execute("SELECT * FROM clientes ORDER BY id DESC")
    lista = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template("clientes.html", clientes=lista)

# --- PETS ---
@app.route("/pets", methods=["GET", "POST"])
def pets():
    conexao = conectar_bd()
    cursor = conexao.cursor(dictionary=True)
    if request.method == "POST":
        nome, tipo, raca, idade, c_id = request.form["nome"], request.form["tipo"], request.form["raca"], request.form["idade"], request.form["cliente_id"]
        cursor.execute("INSERT INTO pets (nome, tipo, raca, idade, cliente_id) VALUES (%s, %s, %s, %s, %s)", (nome, tipo, raca, idade, c_id))
        conexao.commit()
        return redirect(url_for("pets"))
    
    cursor.execute("SELECT * FROM pets")
    lista_pets = cursor.fetchall()
    cursor.execute("SELECT id, nome FROM clientes")
    lista_clientes = cursor.fetchall()
    return render_template("pets.html", pets=lista_pets, clientes=lista_clientes)

# --- SERVIÇOS ---
@app.route("/servicos", methods=["GET", "POST"])
def servicos():
    conexao = conectar_bd()
    cursor = conexao.cursor(dictionary=True)
    if request.method == "POST":
        p_id, tipo, data, valor = request.form["pet_id"], request.form["tipo_servico"], request.form["data"], request.form["valor"]
        cursor.execute("INSERT INTO servicos (pet_id, tipo_servico, data_servico, valor) VALUES (%s, %s, %s, %s)", (p_id, tipo, data, valor))
        conexao.commit()
        return redirect(url_for("servicos"))
    
    cursor.execute("SELECT * FROM servicos")
    lista_servicos = cursor.fetchall()
    cursor.execute("SELECT id, nome FROM pets")
    lista_pets = cursor.fetchall()
    return render_template("servicos.html", servicos=lista_servicos, pets=lista_pets)

# --- PRODUTOS ---
@app.route("/produtos", methods=["GET", "POST"])
def produtos():
    conexao = conectar_bd()
    cursor = conexao.cursor(dictionary=True)
    if request.method == "POST":
        nome, desc, preco, qtd = request.form["nome"], request.form["descricao"], request.form["preco"], request.form["quantidade"]
        cursor.execute("INSERT INTO produtos (nome, descricao, preco, quantidade_estoque) VALUES (%s, %s, %s, %s)", (nome, desc, preco, qtd))
        conexao.commit()
        return redirect(url_for("produtos"))
    
    cursor.execute("SELECT * FROM produtos")
    lista_produtos = cursor.fetchall()
    return render_template("produtos.html", produtos=lista_produtos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)