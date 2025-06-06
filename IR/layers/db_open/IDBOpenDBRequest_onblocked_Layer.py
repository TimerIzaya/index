from IR.IRNodes import AssignmentExpression, FunctionExpression, Identifier, MemberExpression, CallExpression, Literal
from IR.IRType import IDBOpenDBRequest
from IR.layers.Globals import Global
from IR.layers.Layer import Layer, LayerType
from IR.layers.LayerBuilder import LayerBuilder


class IDBOpenDBRequest_onblocked_Layer(LayerBuilder):

    name = "IDBOpenDBRequest_onblocked_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build():
        body = [
            CallExpression(Identifier("console"), "log", [Literal("open db blocked triggered")])
        ]

        # request.onblocked = function(event) { ... }
        open_request_id = Global.irctx.get_identifier_by_type(IDBOpenDBRequest)
        handler = AssignmentExpression(
            left=MemberExpression(open_request_id, "onblocked"),
            right=FunctionExpression([Identifier("event")], body)
        )

        return Layer(
            IDBOpenDBRequest_onblocked_Layer.name,
            ir_nodes=[handler],
            layer_type=IDBOpenDBRequest_onblocked_Layer.layer_type
        )
