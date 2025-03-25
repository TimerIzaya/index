from IR.IRNodes import CallExpression
from IR.IRContext import IRContext, Variable
from IR.IRParamGenerator import ParameterGenerator
from IR.IRType import IDBTransaction
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.IDBTransaction_ObjectStoreAccess_Layer import IDBTransaction_ObjectStoreAccess_Layer


class IDBDatabase_Transaction_Layer(LayerBuilder):
    name = "IDBDatabase_Transaction_Layer"
    layer_type = LayerType.CALLING

    @staticmethod
    def build(ctx: IRContext) -> Layer:
        gen = ParameterGenerator(ctx)

        store_name = gen.generate_value_from_typename("string")
        txn_mode = gen.generate_value_from_typename("string")

        call = CallExpression(
            callee_object=ctx.get_random_identifier("IDBDatabase"),
            callee_method="transaction",
            args=[store_name, txn_mode],
            result_name="txn"
        )

        ctx.register_variable(Variable("txn", IDBTransaction))
        access_layer = IDBTransaction_ObjectStoreAccess_Layer.build(ctx)

        return Layer(IDBDatabase_Transaction_Layer.name, [call], children=[access_layer], layer_type=LayerType.CALLING)
