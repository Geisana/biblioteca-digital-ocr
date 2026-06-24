from ocr.factory import OCRFactory

class TesseractPuro:

    def executar(
        self,
        paginas
    ):

        ocr = OCRFactory.criar(
            "tesseract"
        )

        return ocr.executar(
            paginas
        )