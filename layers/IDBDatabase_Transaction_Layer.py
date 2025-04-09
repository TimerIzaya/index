from IR.IRContext import IRContext, Variable
from IR.IRNodes import AssignmentExpression, CallExpression, Identifier, Literal
from IR.IRType import IDBTransaction
from layers.IDBContext import IDBContext
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.IDBTransaction_ObjectStoreAccess_Layer import IDBTransaction_ObjectStoreAccess_Layer


class IDBDatabase_Transaction_Layer(LayerBuilder):
    name = "IDBDatabase_Transaction_Layer"
    layer_type = LayerType.CALLING

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        # ✅ 从 IDBContext 中获取当前已注册的 object store
        store_name = idbctx.pick_random_object_store()
        txn_mode = Literal("readwrite")  # 可扩展为枚举

        call = CallExpression(
            callee_object=Identifier("db"),
            callee_method="transaction",
            args=[Literal(store_name), txn_mode],
            result_name="txn"
        )

        irctx.register_variable(Variable("txn", IDBTransaction))

        # 创建子层，访问 objectStore 并执行数据操作
        child_layer = IDBTransaction_ObjectStoreAccess_Layer.build(irctx, idbctx)

        return Layer(
            name=IDBDatabase_Transaction_Layer.name,
            ir_nodes=[call],
            children=[child_layer],
            layer_type=IDBDatabase_Transaction_Layer.layer_type
        )
