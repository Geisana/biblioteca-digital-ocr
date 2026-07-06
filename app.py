from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    send_file,
    send_from_directory
)
from pipelines.factory import PipelineFactory
import platform
from services.metrics import calcular_metricas
from dotenv import load_dotenv

from flask_sqlalchemy import SQLAlchemy

from pdf2image import convert_from_path

from functools import wraps

import os

from services.ocr_service import OCRService
from services.ia_service import gerar_resumo

# ============================================
# CONFIGURAÇÕES
# ============================================

load_dotenv()

USUARIO_ADMIN = "admin"
SENHA_ADMIN = "1234"

import platform

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if platform.system() == "Windows":

    POPPLER_PATH = os.path.join(
        BASE_DIR,
        "poppler",
        "poppler-26.02.0",
        "Library",
        "bin"
    )

else:

    POPPLER_PATH = None


print("Sistema:", platform.system())
print("BASE_DIR:", BASE_DIR)
print("POPPLER_PATH:", POPPLER_PATH)

if POPPLER_PATH:
    print("EXISTE:", os.path.exists(POPPLER_PATH))


UPLOAD_FOLDER = "uploads"

# ============================================
# FLASK
# ============================================

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ============================================
# PASTAS
# ============================================

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

os.makedirs("uploads/paginas", exist_ok=True)

# ============================================
# LOGIN DECORATOR
# ============================================

def login_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        if not session.get("logado"):
            return redirect("/login")

        return f(*args, **kwargs)

    return wrapper

# ============================================
# MODELO DOCUMENTO
# ============================================

class Documento(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome_arquivo = db.Column(
        db.String(200)
    )

    titulo = db.Column(
        db.String(300)
    )

    data_documento = db.Column(
        db.String(50)
    )

    autoria = db.Column(
        db.String(200)
    )

    caminho_pdf = db.Column(
        db.String(300)
    )

    caminho_thumb = db.Column(
        db.String(300)
    )

    texto_ocr = db.Column(
        db.Text
    )

    resumo = db.Column(
        db.Text
    )

    total_paginas = db.Column(
        db.Integer
    )

    tempo_total_ocr = db.Column(
        db.Float
    )

    tempo_medio_pagina = db.Column(
        db.Float
    )

    cer = db.Column(
        db.Float
    )

    wer = db.Column(
        db.Float
    )

    taxa_sucesso = db.Column(
        db.Float
    )

    data_upload = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    pipeline = db.Column(
    db.String(150)
)


    paginas = db.relationship(
        "Pagina",
        backref="documento",
        lazy=True,
        cascade="all, delete-orphan"
    )


# ============================================
# MODELO PAGINA
# ============================================

class Pagina(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    documento_id = db.Column(
        db.Integer,
        db.ForeignKey("documento.id"),
        nullable=False
    )

    numero_pagina = db.Column(
        db.Integer,
        nullable=False
    )

    caminho_imagem = db.Column(
        db.String(300)
    )

    texto_ocr = db.Column(
        db.Text
    )

# ============================================
# HOME
# ============================================

@app.route("/")
def home():

    busca = request.args.get("busca")

    if busca:

        documentos = Documento.query.filter(
            Documento.texto_ocr.contains(busca)
        ).order_by(
            Documento.id.desc()
        ).all()

    else:

        documentos = Documento.query.order_by(
            Documento.id.desc()
        ).all()

    return render_template(
        "index.html",
        documentos=documentos
    )

# ============================================
# UPLOAD
# ============================================
ocr_service = OCRService()

@app.route("/upload", methods=["POST"])
def upload():

    arquivo = request.files["pdf"]

    titulo = request.form.get("titulo")

    data_documento = request.form.get("data_documento")

    autoria = request.form.get("autoria")

    if arquivo.filename == "":
        return "Nenhum arquivo enviado"
    
    # ============================================
    # SALVAR PDF
    # ============================================

    caminho_pdf = os.path.join(
        UPLOAD_FOLDER,
        arquivo.filename
    )

    arquivo.save(caminho_pdf)

    # ============================================
    # CONVERTER PDF EM IMAGENS
    # ============================================

    paginas_pdf = convert_from_path(
        caminho_pdf,
        dpi=300,
        poppler_path=POPPLER_PATH
    )

    total_paginas = len(paginas_pdf)

    # ============================================
    # CRIAR THUMBNAIL
    # ============================================

    pagina1 = paginas_pdf[0]

    nome_thumb = f"thumb_{arquivo.filename}.jpg"

    caminho_thumb = os.path.join(
        UPLOAD_FOLDER,
        nome_thumb
    )

    pagina1.save(
        caminho_thumb,
        "JPEG"
    )
    import cv2

    

    # ============================================
    # OCR
    # ============================================
    codigo_pipeline = request.form.get("pipeline")
    print("PIPELINE RECEBIDO:", codigo_pipeline)

    codigo_pipeline = request.form.get("pipeline")
    pipeline = PipelineFactory.criar(codigo_pipeline)
    modelo = "tesseract"

    resultado_ocr = ocr_service.executar(
    paginas_pdf,
    pipeline = pipeline
        )

    texto_total = resultado_ocr["texto"]

    tempo_total = resultado_ocr["tempo_total"]

    tempo_medio = resultado_ocr["tempo_medio"]

    # ============================================
    # GROUND TRUTH
    # ============================================

    nome_txt = arquivo.filename.replace(
        ".pdf",
        ".txt"
    )

    caminho_txt = os.path.join(
        "dataset",
        nome_txt
    )

    metricas = {
        "cer": None,
        "wer": None,
        "sucesso": None
    }

    if os.path.exists(caminho_txt):

        with open(
            caminho_txt,
            "r",
            encoding="utf-8"
        ) as f:

            ground_truth = f.read()

        metricas = calcular_metricas(
            ground_truth,
            texto_total
        )

    # ============================================
    # RESUMO IA
    # ============================================

    resumo = gerar_resumo(
        texto_total
    )
    

    # ============================================
    # SALVAR DOCUMENTO
    # ============================================

    doc = Documento(

    nome_arquivo=arquivo.filename,

    titulo=titulo,

    data_documento=data_documento,

    autoria=autoria,

    caminho_pdf=caminho_pdf,

    caminho_thumb=nome_thumb,

    texto_ocr=texto_total,

    resumo=resumo,

    total_paginas=total_paginas,

    tempo_total_ocr=tempo_total,

    tempo_medio_pagina=tempo_medio,

    cer=metricas["cer"],

    wer=metricas["wer"],

    taxa_sucesso=metricas["sucesso"],

    pipeline=pipeline.nome
)
    print("Salvando documento...")
    print(caminho_txt)
    print(os.path.exists(caminho_txt))
    print(doc.nome_arquivo)
    print(doc.cer)
    print(doc.wer)

    db.session.add(doc)

    db.session.commit()
    print("Documento salvo!")
    
    # ============================================
    # SALVAR PÁGINAS
    # ============================================

    for i, pagina in enumerate(paginas_pdf):

        numero = i + 1

        nome_imagem = (
            f"doc_{doc.id}_pagina_{numero}.jpg"
        )

        caminho_imagem = os.path.join(
            "uploads/paginas",
            nome_imagem
        )

        pagina.save(
            caminho_imagem,
            "JPEG"
        )

        texto_pagina = ocr_service.executar(
            [pagina],
            pipeline= pipeline
        )

        if isinstance(texto_pagina, dict):
            texto_pagina = texto_pagina["texto"]

        pagina_db = Pagina(

            documento_id=doc.id,

            numero_pagina=numero,

            caminho_imagem=nome_imagem,

            texto_ocr=texto_pagina
        )

        db.session.add(pagina_db)

    db.session.commit()

    return redirect(
        "/admin/documentos"
    )


# ============================================
# DOCUMENTO
# ============================================

@app.route("/documento/<int:id>")
def documento(id):

    doc = Documento.query.get_or_404(id)

    return render_template(
        "documento.html",
        documento=doc
    )

# ============================================
# ADMIN
# ============================================

@app.route("/admin")
@login_required
def admin():

    documentos = Documento.query.order_by(
        Documento.id.desc()
    ).all()

    return render_template(
        "admin/dashboard.html",
        documentos=documentos
    )

# ============================================
# ADMIN UPLOAD
# ============================================

@app.route("/admin/upload")
@login_required
def admin_upload():

    return render_template(
        "admin/upload.html",
        pipelines=PipelineFactory.listar()
    )

# ============================================
# ADMIN DOCUMENTOS
# ============================================

@app.route("/admin/documentos")
@login_required
def admin_documentos():

    documentos = Documento.query.order_by(
        Documento.id.desc()
    ).all()

    return render_template(
        "admin/documentos.html",
        documentos=documentos
    )

# ============================================
# DELETE
# ============================================

@app.route("/admin/delete/<int:id>")
@login_required
def delete(id):

    doc = Documento.query.get_or_404(id)

    db.session.delete(doc)

    db.session.commit()

    return redirect(
        "/admin/documentos"
    )

# ============================================
# PDF
# ============================================

@app.route("/pdf/<int:id>")
def pdf(id):

    doc = Documento.query.get_or_404(id)

    return send_file(
        doc.caminho_pdf
    )

# ============================================
# UPLOADS
# ============================================

@app.route("/uploads/<path:filename>")
def uploads(filename):

    return send_from_directory(
        "uploads",
        filename
    )

# ============================================
# LOGIN
# ============================================

@app.route("/login", methods=["GET", "POST"])
def login():

    erro = None

    if request.method == "POST":

        usuario = request.form["usuario"]

        senha = request.form["senha"]

        if (
            usuario == USUARIO_ADMIN
            and
            senha == SENHA_ADMIN
        ):

            session["logado"] = True

            return redirect("/admin")

        else:

            erro = "Usuário ou senha inválidos"

    return render_template(
        "login.html",
        erro=erro
    )

# ============================================
# LOGOUT
# ============================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

# ============================================
# START
# ============================================

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)