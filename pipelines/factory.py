from pipelines.tesseract_puro import (
    TesseractPuro
)
from pipelines.tesseract_preprocessado import TesseractPreprocessado
class PipelineFactory:

    @staticmethod
    def criar(nome):

        pipelines = {
            "tesseract_puro": TesseractPuro,
            #"tesseract_grayscale": TesseractGrayscale,
            #"tesseract_threshold": TesseractThreshold,
            "tesseract_preprocessado": TesseractPreprocessado,
}

        return pipelines[nome]()