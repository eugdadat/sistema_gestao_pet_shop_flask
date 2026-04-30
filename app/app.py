from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import time

app = Flask(__name__)

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
        except mysql.connector.Error:
            tentativas-= 1
            time.sleep(3)
    return None

@app.route("/")
def index():
    return render_template("idex.html")

@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    conexao = conectar_bd()
    if not conexao:
        return "Erro de conexão com o banco de dados."
    
    cursor = conexao.cursor(dictionary=True)

    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        cursor.execute(
            "INSERT INTO cliente (nome, telefone, email) VALUES (%s, %s, %s)",
            (nome, telefone, email)
        )
        conexao.commit()
        return redirect(url_for("clientes"))
    
    cursor.execute("SELECT *FROM clientes ORDER BY id")
    lista_clientes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("clientes.html", clientes=lista_clientes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)