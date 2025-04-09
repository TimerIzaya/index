from IR.IRContext import IRContext
from IR.IRNodes import AssignmentExpression, FunctionExpression
from layers.IDBContext import IDBContext
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder


class IDBOpenDBRequest_onerror_Layer(LayerBuilder):
    name = "IDBOpenDBRequest_onerror_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        handler = AssignmentExpression(
            target="request.onerror",
            value=FunctionExpression(params=["event"], body=[])
        )
        return Layer(IDBOpenDBRequest_onerror_Layer.name, [handler], layer_type=LayerType.REGISTER)
