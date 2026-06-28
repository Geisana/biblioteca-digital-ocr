# pipelines/tesseract_avancado.py
from pipelines.base import BasePipeline
import pytesseract
import numpy as np

# Importamos as nossas peças de Lego!
from preprocessamento.filtros import para_cinza, binarizar, remover_ruido

class Pipeline03(BasePipeline):

    def __init__(self):
        self.codigo = "pipeline_03"
        self.nome = "Tesseract (Alta Limpeza)"
        self.descricao = "Aplica remoção de ruído, escala de cinza e binarização de Otsu."

    def extrair_texto_pagina(self, pagina):
        # Transforma a imagem PIL do PDF em um formato que o OpenCV aceita
        img_array = np.array(pagina)

        # 1. A LINHA DE MONTAGEM DOS FILTROS (O Combo!)
        img_limpa = remover_ruido(img_array)
        img_cinza = para_cinza(img_limpa)
        img_final = binarizar(img_cinza)
        
        # 2. O Tesseract lê a imagem perfeitamente tratada
        texto = pytesseract.image_to_string(
            img_final,
            lang="por"
        )
        
        return texto