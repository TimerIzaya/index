from abc import ABC, abstractmethod
from IR.IRContext import IRContext
from layers.Layer import Layer, LayerType

class LayerBuilder(ABC):
    name: str
    layer_type: LayerType

    @staticmethod
    @abstractmethod
    def build(ctx: IRContext) -> Layer:
        pass
