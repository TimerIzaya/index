from IR.IRNodes import AssignmentExpression, FunctionExpression, MemberExpression
from IR.IRContext import IRContext, Variable
from IR.IRType import IDBDatabase
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.IDBDatabase_Transaction_Layer import IDBDatabase_Transaction_Layer


class IDBOpenDBRequest_onsuccess_Layer(LayerBuilder):

    name = "IDBOpenDBRequest_onsuccess_Layer"

    layer_type = LayerType.REGISTER

    @staticmethod
    def build(ctx: IRContext) -> Layer:
        ctx.enter_layer(IDBOpenDBRequest_onsuccess_Layer)

        assign_result = AssignmentExpression("db", MemberExpression("openRequest", "result"))
        ctx.register_variable(Variable("db", IDBDatabase))

        txn_layer = IDBDatabase_Transaction_Layer.build(ctx)
        func = FunctionExpression([], [assign_result] + txn_layer.ir_nodes)
        handler = AssignmentExpression("openRequest.onsuccess", func)

        ctx.exit_layer()
        return Layer(IDBOpenDBRequest_onsuccess_Layer.name, [handler], children=[txn_layer], layer_type=LayerType.REGISTER)
