# pipelines/tesseract_avancado.py
from pipelines.base import BasePipeline
import pytesseract
import numpy as np

from preprocessamento.filtros import para_cinza, binarizar, remover_ruido, aumentar_resolucao, aumentar_contraste, remover_ruido_bilateral
class Pipeline04(BasePipeline):

    def __init__(self):
        self.codigo = "pipeline_04"
        self.nome = "Documentos Históricos"
        self.descricao = ""

    def extrair_texto_pagina(self, pagina):
            img_array = np.array(pagina)
            img_cinza = para_cinza(img_array)
            img_resolucao = aumentar_resolucao(img_cinza, escala=2.0) # Aumentar um pouco mais
            img_contraste = aumentar_contraste(img_resolucao)
            
            # REMOVER RUÍDO COM FILTRO BILATERAL (Mais preciso que o MedianBlur)
            img_limpa = remover_ruido_bilateral(img_contraste)
            
            # AQUI VOCÊ PODE TENTAR LER SEM A BINARIZAÇÃO (Otsu)
            texto = pytesseract.image_to_string(img_limpa, lang="por")
            return texto