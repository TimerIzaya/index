from IR.IRContext import IRContext, Variable
from IR.IRType import IDBObjectStore
from IR.IRNodes import AssignmentExpression, CallExpression, Identifier, Literal
from layers.IDBContext import IDBContext
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.IDBObjectStore_DataOps_Layer import IDBObjectStore_DataOps_Layer


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

        assign = AssignmentExpression(
            left=Identifier("store"),
            right=call
        )

        irctx.register_variable(Variable("store", IDBObjectStore))

        child = IDBObjectStore_DataOps_Layer.build(irctx, idbctx)
        return Layer(
            IDBTransaction_ObjectStoreAccess_Layer.name,
            ir_nodes=[assign],
            children=[child],
            layer_type=IDBTransaction_ObjectStoreAccess_Layer.layer_type
        )
