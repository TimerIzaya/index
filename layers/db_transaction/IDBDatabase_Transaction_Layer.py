from IR.IRContext import IRContext, Variable
from IR.IRType import IDBTransaction
from IR.IRNodes import CallExpression, Identifier, Literal
from layers.IDBContext import IDBContext
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.db_transaction.db_curd.IDBTransaction_ObjectStoreAccess_Layer import IDBTransaction_ObjectStoreAccess_Layer
from layers.db_transaction.IDBTransaction_oncomplete_Layer import IDBTransaction_oncomplete_Layer
from layers.db_transaction.IDBTransaction_onabort_Layer import IDBTransaction_onabort_Layer
from layers.db_transaction.IDBTransaction_onerror_Layer import IDBTransaction_onerror_Layer


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

        # 注册 txn 变量
        irctx.register_variable(Variable("txn", IDBTransaction))

        # 构造子层级
        children = [
            IDBTransaction_ObjectStoreAccess_Layer.build(irctx, idbctx),
            IDBTransaction_oncomplete_Layer.build(irctx, idbctx),
            IDBTransaction_onabort_Layer.build(irctx, idbctx),
            IDBTransaction_onerror_Layer.build(irctx, idbctx),
        ]

        return Layer(
            IDBDatabase_Transaction_Layer.name,
            ir_nodes=[call],
            children=children,
            layer_type=IDBDatabase_Transaction_Layer.layer_type
        )
