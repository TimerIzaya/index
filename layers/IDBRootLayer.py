from IR.IRContext import IRContext, Variable
from IR.IRType import IDBFactory
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder

class IDBRootLayer(LayerBuilder):
    name = "IDBRootLayer"
    layer_type = LayerType.CALLING

    @staticmethod
    def build(ctx: IRContext) -> Layer:
        ctx.register_variable(Variable("indexedDB", IDBFactory))
        return Layer(IDBRootLayer.name, [], layer_type=IDBRootLayer.layer_type)
