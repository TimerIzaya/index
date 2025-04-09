from abc import ABC, abstractmethod
from IR.IRContext import IRContext
from layers.IDBContext import IDBContext
from layers.Layer import Layer, LayerType

class LayerBuilder(ABC):

    name: str

    layer_type: LayerType

    @staticmethod
    @abstractmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        pass
