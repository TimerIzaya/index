from IR.IRNodes import AssignmentExpression, FunctionExpression, Identifier, MemberExpression, CallExpression, Literal
from IR.IRType import IDBOpenDBRequest, IDBDatabase
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder


class IDBOpenDBRequest_onerror_Layer(LayerBuilder):

    name = "IDBOpenDBRequest_onerror_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build(irctx, idbctx):
        body = [
            CallExpression(Identifier("console"), "log", [Literal("open db onerror triggered")]),
        ]
        # request.onerror = function(event) { ... }
        open_request_id = irctx.get_identifier_by_type(IDBOpenDBRequest)
        handler = AssignmentExpression(
            left=MemberExpression(open_request_id, "onerror"),
            right=FunctionExpression([Identifier("event")], body)
        )

        return Layer(
            IDBOpenDBRequest_onerror_Layer.name,
            ir_nodes=[handler],
            layer_type=IDBOpenDBRequest_onerror_Layer.layer_type
        )
