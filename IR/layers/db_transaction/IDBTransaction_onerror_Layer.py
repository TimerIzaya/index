from IR.layers.Globals import Global
from IR.IRNodes import AssignmentExpression, MemberExpression, Identifier, FunctionExpression, ConsoleLog, Literal
from IR.layers.Layer import Layer, LayerType
from IR.layers.LayerBuilder import LayerBuilder
from IR.type.IDBType import IDBType


class IDBTransaction_onerror_Layer(LayerBuilder):
    name = "IDBTransaction_onerror_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build() -> Layer:
        txn = Global.irctx.get_identifier_by_type(IDBType.IDBTransaction)
        handler = AssignmentExpression(
            left=MemberExpression(txn, "onerror"),
            right=FunctionExpression(
                params=[Identifier("event")],
                body=[ConsoleLog(Literal("Transaction error occurred"))]
            )
        )
        return Layer(IDBTransaction_onerror_Layer.name, [handler], layer_type=IDBTransaction_onerror_Layer.layer_type)
