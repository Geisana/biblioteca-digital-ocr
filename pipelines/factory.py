from pipelines.tesseract_puro import (
    TesseractPuro
)

class PipelineFactory:

    @staticmethod
    def criar(nome):

        pipelines = {

            "tesseract_puro":
                TesseractPuro

        }

        return pipelines[nome]()