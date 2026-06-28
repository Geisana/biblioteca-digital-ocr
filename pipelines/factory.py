from pipelines.pipeline_01 import Pipeline01
from pipelines.pipeline_02 import Pipeline02
from pipelines.pipeline_03 import Pipeline03
from pipelines.pipeline_04 import Pipeline04
from pipelines.pipeline_05 import Pipeline05



class PipelineFactory:

    _pipelines = {
        "pipeline_01": Pipeline01,
        "pipeline_02": Pipeline02,
        "pipeline_03": Pipeline03,
        "pipeline_04": Pipeline04,
        "pipeline_05": Pipeline05,
    }

    @classmethod
    def criar(cls, codigo):

        if codigo not in cls._pipelines:
            raise ValueError("Pipeline não encontrado")

        return cls._pipelines[codigo]()  # <- aqui cria a instância
    
    @classmethod
    def listar(cls):
        return [
            {
                "codigo": k,
                "nome": v().nome,
                "descricao": v().descricao
            }
            for k, v in cls._pipelines.items()
        ]