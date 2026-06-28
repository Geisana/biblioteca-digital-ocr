from pipelines.base import BasePipeline
import pytesseract
import numpy as np

from preprocessamento.filtros import para_cinza, binarizar, remover_ruido, aumentar_resolucao, aumentar_contraste, remover_ruido_bilateral, detectar_caixas_texto
class Pipeline05(BasePipeline):

    def __init__(self):
        self.codigo = "pipeline_05"
        self.nome = "EastOCR"
        self.descricao = ""


    def extrair_texto_pagina(self, pagina):
            img = np.array(pagina)
            caixas = detectar_caixas_texto(img)
            
            texto_completo = []
            for (x, y, w, h) in caixas:
                # 1. Validação: garante que o recorte é válido e tem tamanho
                if w <= 0 or h <= 0:
                    continue
                
                # 2. Garante que as coordenadas não saiam da imagem
                # Isso evita erros de recorte fora dos limites (out of bounds)
                recorte = img[max(0, y):max(0, y)+h, max(0, x):max(0, x)+w]
                
                if recorte.size == 0:
                    continue
                    
                recorte_cinza = para_cinza(recorte)
                
                # 3. Proteção extra: apenas envia para o Tesseract se não estiver vazio
                if recorte_cinza is not None and recorte_cinza.size > 0:
                    bloco_texto = pytesseract.image_to_string(recorte_cinza, lang="por")
                    texto_completo.append(bloco_texto)
                
            return "\n".join(texto_completo)