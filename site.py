from flask import Flask, render_template, request
from datetime import datetime
from fpdf import FPDF

app = Flask(__name__)

@app.route("/")
def pag_inicial():
    return render_template("index.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/registro", methods = ["GET", "POST"])
def registro():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        if email == "" or senha == "":
            return render_template("campos_requisitados.html")

        elif any(x.isupper() for x in senha):
            registro = email + ' - ' + senha + '\n'
            login = open("login.txt", "a")
            login.write(registro)
            return render_template("login.html")

        else:
            return render_template("senha_maiuscula.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/entrar", methods = ["GET", "POST"])
def entrar():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        registro = email + ' - ' + senha + '\n'

        arquivo = open("login.txt", "r")
        lista = arquivo.readlines()

        if registro in lista:
            return render_template("carta.html")
        
        else:
            return render_template("usuario_nao_identificado.html")


@app.route("/texto", methods = ["GET", "POST"])
def texto():
    if request.method == "POST":
        data = request.form.get("data")
        destinatario = request.form.get("destinatario")
        mensagem = request.form.get("mensagem")
        remetente = request.form.get("remetente")

        if data == "" or destinatario == ""  or mensagem == "" or remetente == "":
            return "<h1>Você não preencheu todos os espaços!</h1>"
        else:
            hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nome_arquivo_txt = f"carta_{hora}.txt"
            nome_arquivo_pdf = f"carta_{hora}.pdf"
            
            with open(nome_arquivo_txt, "w") as arquivo:
                carta = f"Data: {data}\nDestinatário: {destinatario}\nMensagem: {mensagem}\nRemetente: {remetente}\n"
                arquivo.write(carta)
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            with open(nome_arquivo_txt, "r") as arquivo_txt:
                for linha in arquivo_txt:
                    pdf.cell(200, 10, txt=linha, ln=True)
            pdf.output(nome_arquivo_pdf)
            
            return render_template("carta_enviada.html")
            
if __name__ == "__main__":
    app.run(debug=True)