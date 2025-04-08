from IR.IRNodes import AssignmentExpression, FunctionExpression
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder


class IDBOpenDBRequest_onblocked_Layer(LayerBuilder):
    name = "IDBOpenDBRequest_onblocked_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build(ctx) -> Layer:
        handler = AssignmentExpression(
            target="request.onblocked",
            value=FunctionExpression(params=["event"], body=[])
        )
        return Layer(IDBOpenDBRequest_onblocked_Layer.name, [handler], layer_type=LayerType.REGISTER)
