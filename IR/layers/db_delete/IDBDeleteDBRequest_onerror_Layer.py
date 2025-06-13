from IR.IRNodes import FunctionExpression, AssignmentExpression, MemberExpression, Identifier, Literal, CallExpression
from IR.layers.Globals import Global
from IR.type.IDBType import IDBType
from config import randomFuzzing
from IR.layers.Layer import Layer, LayerType
from IR.layers.LayerBuilder import LayerBuilder


class IDBDeleteDBRequest_onerror_Layer(LayerBuilder):
    
    name = "IDBDeleteDBRequest_onerror_Layer"

    layer_type = LayerType.REGISTER

    @staticmethod
    def build() -> Layer:
        body = [
            CallExpression(Identifier("console"), "log", [Literal("delete db onerror triggered")])
        ]

        if randomFuzzing:
            handler = AssignmentExpression(
                left=MemberExpression(Global.irctx.get_identifier_by_type(IDBType.IDBOpenDBRequest), "onerror"),
                right=FunctionExpression([Identifier("event")], body)
            )
        else:
            # just for debug
            handler = AssignmentExpression(
                left=MemberExpression(Identifier("deleteRequest"), "onerror"),
                right=FunctionExpression([Identifier("event")], body)
            )

        return Layer(
            IDBDeleteDBRequest_onerror_Layer.name,
            ir_nodes=[handler],
            children=[],
            layer_type=IDBDeleteDBRequest_onerror_Layer.layer_type
        )
