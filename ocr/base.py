from abc import ABC, abstractmethod

class OCRBase(ABC):

    @abstractmethod
    def executar(self, imagem):
        pass