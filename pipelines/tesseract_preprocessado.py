from pipelines.preprocessamento import grayscale, threshold
from ocr.tesseract.engine import TesseractOCR

class TesseractPreprocessado:

    def __init__(self):
        self.ocr = TesseractOCR()

    def executar(self, paginas):

        from pipelines.preprocessamento import grayscale, threshold

        textos = []

        for img in paginas:

            img = grayscale(img)
            img = threshold(img)

            texto = self.ocr.executar([img])  # ou recognize dependendo do seu OCR base

            # caso venha dict
            if isinstance(texto, dict):
                texto = texto["texto"]

            textos.append(texto)

        return {
            "texto": " ".join(textos),
            "tempo_total": 0,
            "tempo_medio": 0
        }