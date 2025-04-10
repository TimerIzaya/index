from IR.IRNodes import AssignmentExpression, FunctionExpression, Identifier, MemberExpression
from IR.IRType import IDBOpenDBRequest
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder


class IDBOpenDBRequest_onblocked_Layer(LayerBuilder):

    name = "IDBOpenDBRequest_onblocked_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build(irctx, idbctx):
        # request.onblocked = function(event) { ... }
        open_request_id = irctx.get_identifier_by_type(IDBOpenDBRequest)
        handler = AssignmentExpression(
            left=MemberExpression(open_request_id, "onblocked"),
            right=FunctionExpression([Identifier("event")], [])
        )

        return Layer(
            IDBOpenDBRequest_onblocked_Layer.name,
            ir_nodes=[handler],
            layer_type=IDBOpenDBRequest_onblocked_Layer.layer_type
        )
