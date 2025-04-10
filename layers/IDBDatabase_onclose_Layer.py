from IR.IRContext import IRContext
from IR.IRType import IDBDatabase
from layers.IDBContext import IDBContext
from IR.IRNodes import Identifier, MemberExpression, AssignmentExpression, FunctionExpression, ConsoleLog, Literal
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder


class IDBDatabase_onclose_Layer(LayerBuilder):
    name = "IDBDatabase_onclose_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        db_id = irctx.get_identifier_by_type(IDBDatabase)

        body = [
            ConsoleLog(Literal("The version of this database has changed"))
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
