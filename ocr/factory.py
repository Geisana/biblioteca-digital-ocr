from ocr.tesseract.engine import TesseractOCR
#from ocr.easyocr.engine import EasyOCR

class OCRFactory:

    @staticmethod
    def criar(nome):

        motores = {
            "tesseract": TesseractOCR,
            #"easyocr": EasyOCR
        }

        return motores[nome]()