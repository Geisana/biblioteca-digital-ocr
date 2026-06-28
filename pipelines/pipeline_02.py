from pipelines.base import BasePipeline
import pytesseract

# Importamos a nossa peça de Lego!
from preprocessamento.filtros import para_cinza

class Pipeline02(BasePipeline):

    def __init__(self):
        self.codigo = "pipeline_02"
        self.nome = "Tesseract Grayscale"
        self.descricao = "Executa o Tesseract com pré-processamento em escala de cinza."

    def extrair_texto_pagina(self, pagina):

        # 1. Aplica o filtro usando a função importada
        imagem_cinza = para_cinza(pagina)
        
        # 2. Extrai o texto da imagem que já está em preto e branco
        texto = pytesseract.image_to_string(
            imagem_cinza,
            lang="por", 
            config="--psm 3"
        )
        
        return texto