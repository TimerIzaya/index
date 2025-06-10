from IR.IRContext import IRContext
from IR.IRType import IDBDatabase
from IR.layers.Globals import Global
from IR.layers.LiteralContext import LiteralContext
from IR.IRNodes import Identifier, MemberExpression, AssignmentExpression, FunctionExpression, ConsoleLog, Literal
from IR.layers.Layer import Layer, LayerType
from IR.layers.LayerBuilder import LayerBuilder


class IDBDatabase_onclose_Layer(LayerBuilder):
    name = "IDBDatabase_onclose_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build() -> Layer:
        db_id = Global.irctx.get_identifier_by_type(IDBDatabase)

        body = [
            ConsoleLog(Literal("The database connection is unexpectedly closed"))
        ]

        handler = AssignmentExpression(
            left=MemberExpression(db_id, "onclose"),
            right=FunctionExpression(
                params=[Identifier("event")],
                body=body
            )
        )

        return Layer(
            IDBDatabase_onclose_Layer.name,
            ir_nodes=[handler],
            layer_type=IDBDatabase_onclose_Layer.layer_type
        )
