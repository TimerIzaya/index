from IR.IRContext import IRContext
from IR.IRType import IDBTransaction
from layers.IDBContext import IDBContext
from IR.IRNodes import AssignmentExpression, MemberExpression, Identifier, FunctionExpression, ConsoleLog, Literal
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder


class IDBTransaction_onabort_Layer(LayerBuilder):
    name = "IDBTransaction_onabort_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        txn = irctx.get_identifier_by_type(IDBTransaction)
        handler = AssignmentExpression(
            left=MemberExpression(txn, "onabort"),
            right=FunctionExpression(
                params=[Identifier("event")],
                body=[ConsoleLog(Literal("Transaction was aborted"))]
            )
        )
        return Layer(IDBTransaction_onabort_Layer.name, [handler], layer_type=IDBTransaction_onabort_Layer.layer_type)
