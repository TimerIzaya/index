from IR.layers.Globals import Global
from IR.IRNodes import AssignmentExpression, MemberExpression, Identifier, FunctionExpression, ConsoleLog, Literal
from IR.layers.Layer import Layer, LayerType
from IR.layers.LayerBuilder import LayerBuilder
from IR.type.IDBType import IDBType


class IDBTransaction_oncomplete_Layer(LayerBuilder):
    name = "IDBTransaction_oncomplete_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build() -> Layer:
        txn = Global.irctx.get_identifier_by_type(IDBType.IDBTransaction)
        handler = AssignmentExpression(
            left=MemberExpression(txn, "oncomplete"),
            right=FunctionExpression(
                params=[Identifier("event")],
                body=[ConsoleLog(Literal("Transaction completed successfully"))]
            )
        )
        return Layer(IDBTransaction_oncomplete_Layer.name, [handler], layer_type=IDBTransaction_oncomplete_Layer.layer_type)
