from ocr.tesseract.engine import (
    TesseractOCR
)

class TesseractPuro:

    def executar(self, paginas):

        ocr = TesseractOCR()

        return ocr.executar(
            paginas
        )