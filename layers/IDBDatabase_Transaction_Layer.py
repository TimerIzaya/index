from IR.IRContext import IRContext, Variable
from IR.IRType import IDBTransaction
from IR.IRNodes import AssignmentExpression, CallExpression, Identifier, Literal
from layers.IDBContext import IDBContext
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.IDBTransaction_ObjectStoreAccess_Layer import IDBTransaction_ObjectStoreAccess_Layer


class IDBDatabase_Transaction_Layer(LayerBuilder):

    name = "IDBDatabase_Transaction_Layer"
    layer_type = LayerType.CALLING

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        # 获取一个 object store 名称
        store_name = idbctx.pick_random_object_store()

        # 构造调用 db.transaction(...)
        call = CallExpression(
            callee_object=Identifier("db"),
            callee_method="transaction",
            args=[Literal(store_name), Literal("readwrite")],
            result_name="txn"
        )

        irctx.register_variable(Variable("txn", IDBTransaction))

        child = IDBTransaction_ObjectStoreAccess_Layer.build(irctx, idbctx)
        return Layer(
            IDBDatabase_Transaction_Layer.name,
            ir_nodes=[call],
            children=[child],
            layer_type=IDBDatabase_Transaction_Layer.layer_type
        )
