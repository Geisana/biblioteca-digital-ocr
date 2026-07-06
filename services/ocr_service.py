from pipelines.factory import (
    PipelineFactory
)

class OCRService:

    def executar(
        self,
        paginas,
        pipeline
    ):

        

        return pipeline.processar(
            paginas, 
            
        )