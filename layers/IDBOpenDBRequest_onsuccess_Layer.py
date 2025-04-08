from IR.IRNodes import (
    AssignmentExpression,
    MemberExpression,
    Identifier,
    FunctionExpression,
    CallExpression,
    Literal
)
from IR.IRContext import IRContext, Variable
from IR.IRType import IDBDatabase, IDBTransaction
from IR.IRParamGenerator import ParameterGenerator
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.IDBTransaction_ObjectStoreAccess_Layer import IDBTransaction_ObjectStoreAccess_Layer


class IDBOpenDBRequest_onsuccess_Layer(LayerBuilder):
    name = "IDBOpenDBRequest_onsuccess_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build(ctx: IRContext) -> Layer:
        gen = ParameterGenerator(ctx)
        body = []

        # db = request.result
        assign_result = AssignmentExpression(
            target="db",
            value=MemberExpression("request", "result")
        )
        ctx.register_variable(Variable("db", IDBDatabase))
        body.append(assign_result)

        # txn = db.transaction(store, mode)
        store_name = gen.generate_value_from_typename("string")
        mode = gen.generate_value_from_typename("string")

        txn_call = CallExpression(
            callee_object=Identifier("db"),
            callee_method="transaction",
            args=[store_name, mode],
            result_name="txn"
        )
        ctx.register_variable(Variable("txn", IDBTransaction))
        body.append(txn_call)

        # 封装事件处理器
        handler = AssignmentExpression(
            target="request.onsuccess",
            value=FunctionExpression(
                params=["event"],
                body=body
            )
        )

        # 子层：txn.objectStore(...)
        txn_child_layer = IDBTransaction_ObjectStoreAccess_Layer.build(ctx)

        return Layer(
            IDBOpenDBRequest_onsuccess_Layer.name,
            [handler],
            children=[txn_child_layer],
            layer_type=LayerType.REGISTER
        )
