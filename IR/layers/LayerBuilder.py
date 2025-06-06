from abc import ABC, abstractmethod
from IR.IRContext import IRContext
from IR.layers.IDBContext import IDBContext
from IR.layers.Layer import Layer, LayerType

class LayerBuilder(ABC):

    name: str

    layer_type: LayerType

    @staticmethod
    @abstractmethod
    def build() -> Layer:
        pass
