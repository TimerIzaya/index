from IR.IRContext import IRContext
from IR.IRNodes import FunctionExpression, AssignmentExpression, MemberExpression, Identifier, Literal, CallExpression
from IR.IRType import IDBOpenDBRequest
from IR.layers.Globals import Global
from config import randomFuzzing
from IR.layers.Layer import Layer, LayerType
from IR.layers.LayerBuilder import LayerBuilder
from IR.layers.LiteralContext import LiteralContext


class IDBDeleteDBRequest_onsuccess_Layer(LayerBuilder):

    name = "IDBDeleteDBRequest_onsuccess_Layer"
    
    layer_type = LayerType.REGISTER

    @staticmethod
    def build() -> Layer:
        body = [
            CallExpression(Identifier("console"), "log", [Literal("delete db onsuccess triggered")])
        ]
        if randomFuzzing:
            handler = AssignmentExpression(
                left=MemberExpression(Global.irctx.get_identifier_by_type(IDBOpenDBRequest), "onsuccess"),
                right=FunctionExpression([Identifier("event")], body)
            )
        else:
            # just for debug
            handler = AssignmentExpression(
                left=MemberExpression(Identifier("deleteRequest"), "onsuccess"),
                right=FunctionExpression([Identifier("event")], body)
            )
        return Layer(
            IDBDeleteDBRequest_onsuccess_Layer.name,
            ir_nodes=[handler],
            children=[],
            layer_type=IDBDeleteDBRequest_onsuccess_Layer.layer_type
        )
