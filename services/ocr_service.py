from pipelines.factory import (
    PipelineFactory
)

class OCRService:

    def executar(
        self,
        paginas,
        pipeline="tesseract"
    ):

        pipe = PipelineFactory.criar(
            pipeline
        )

        return pipe.executar(
            paginas
        )