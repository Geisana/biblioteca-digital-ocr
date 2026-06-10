import easyocr
from ocr.base import OCRBase

class EasyOCR(OCRBase):

    def __init__(self):
        self.reader = easyocr.Reader(["pt"])

    def executar(self, imagem):

        resultado = self.reader.readtext(
            imagem
        )

        texto = " ".join(
            [r[1] for r in resultado]
        )

        return texto