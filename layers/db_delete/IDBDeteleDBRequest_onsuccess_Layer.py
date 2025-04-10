from IR.IRContext import IRContext
from IR.IRNodes import FunctionExpression, AssignmentExpression, MemberExpression, Identifier, Literal, CallExpression
from IR.IRType import IDBOpenDBRequest
from config import randomFuzzing
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.IDBContext import IDBContext


class IDBDeleteDBRequest_onsuccess_Layer(LayerBuilder):

    name = "IDBDeleteDBRequest_onsuccess_Layer"
    
    layer_type = LayerType.REGISTER

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        body = [
            CallExpression(Identifier("console"), "log", [Literal("onsuccess triggered")])
        ]
        if randomFuzzing:
            handler = AssignmentExpression(
                left=MemberExpression(irctx.get_identifier_by_type(IDBOpenDBRequest), "onsuccess"),
                right=FunctionExpression([Identifier("event")], body)
            )
        else:
            # just for debug
            handler = AssignmentExpression(
                left=MemberExpression(Identifier("deleteRequest"), "onblocked"),
                right=FunctionExpression([Identifier("event")], body)
            )
        return Layer(
            IDBDeleteDBRequest_onsuccess_Layer.name,
            ir_nodes=[handler],
            children=[],
            layer_type=IDBDeleteDBRequest_onsuccess_Layer.layer_type
        )
