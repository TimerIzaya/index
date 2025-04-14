from IR.IRContext import IRContext, Variable
from IR.IRType import IDBObjectStore
from IR.IRNodes import CallExpression, Identifier, Literal
from layers.IDBContext import IDBContext
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.db_transaction.db_curd.IDBObjectStore_CursorOps_Layer import IDBObjectStore_CursorOps_Layer
from layers.db_transaction.db_curd.IDBObjectStore_DataOps_Layer import IDBObjectStore_DataOps_Layer


class IDBTransaction_ObjectStoreAccess_Layer(LayerBuilder):

    name = "IDBTransaction_ObjectStoreAccess_Layer"
    layer_type = LayerType.ACCESS

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        store_name = idbctx.pick_random_object_store()

        call = CallExpression(
            callee_object=Identifier("txn"),
            callee_method="objectStore",
            args=[Literal(store_name)],
            result_name="store"
        )

        irctx.register_variable(Variable("store", IDBObjectStore))

        idbctx.register_object_store(store_name)

        children = [
            IDBObjectStore_DataOps_Layer.build(irctx, idbctx),
            IDBObjectStore_CursorOps_Layer.build(irctx, idbctx),
        ]
        return Layer(
            IDBTransaction_ObjectStoreAccess_Layer.name,
            ir_nodes=[call],
            children=children,
            layer_type=IDBTransaction_ObjectStoreAccess_Layer.layer_type
        )
