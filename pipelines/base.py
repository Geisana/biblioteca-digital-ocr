import time
import time
import platform
import pytesseract

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
class BasePipeline:

    codigo = ""
    nome = ""
    descricao = ""

    def processar(self, paginas):
        texto_total = ""
        tempo_total = 0.0

        # Proteção contra PDFs vazios
        if not paginas:
            return {
                "texto": "",
                "tempo_total": 0.0,
                "tempo_medio": 0.0
            }

        # O laço e o cronômetro agora moram aqui na Base!
        for pagina in paginas:
            inicio = time.time()
            
            # Aqui está a mágica: ele chama um método que ainda não existe na base,
            # mas que obrigatoriamente existirá nos arquivos dos pipelines filhos.
            texto_pagina = self.extrair_texto_pagina(pagina)
            
            fim = time.time()
            
            tempo_total += (fim - inicio)
            texto_total += str(texto_pagina) + "\n\n"

        tempo_medio = tempo_total / len(paginas)

        # Retorna o dicionário redondinho para o app.py salvar no banco
        return {
            "texto": texto_total.strip(),
            "tempo_total": round(tempo_total, 2),
            "tempo_medio": round(tempo_medio, 2)
        }

    def extrair_texto_pagina(self, pagina):
        """
        Método obrigatório: cada pipeline filho (como Pipeline01) 
        DEVE implementar essa função para dizer COMO extrai o texto de UMA imagem.
        """
        raise NotImplementedError("O pipeline filho deve implementar o método 'extrair_texto_pagina'")