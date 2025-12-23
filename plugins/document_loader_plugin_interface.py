from abc import ABC, abstractmethod

class DocumentLoaderPluginInterface(ABC):

    @abstractmethod
    def run(self) -> str:
        pass