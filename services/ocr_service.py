from ocr.factory import (
    OCRFactory
)

class OCRService:

    def executar(
        self,
        paginas,
        modelo="tesseract"
    ):

        ocr = OCRFactory.criar(
            modelo
        )

        return ocr.executar(
            paginas
        )