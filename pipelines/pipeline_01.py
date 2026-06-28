# pipelines/pipeline_01.py

from pipelines.base import BasePipeline
import pytesseract

class Pipeline01(BasePipeline):

    def __init__(self):
        self.codigo = "pipeline_01"
        self.nome = "Tesseract Padrão"
        self.descricao = "Extração direta de texto usando Tesseract OCR"

    def extrair_texto_pagina(self, pagina):
        # A BasePipeline manda uma página pra cá, a gente lê e devolve só o texto.
        texto = pytesseract.image_to_string(
            pagina,
            lang="por"
        )
        return texto