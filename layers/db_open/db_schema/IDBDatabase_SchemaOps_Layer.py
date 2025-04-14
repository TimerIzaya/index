from IR.IRContext import IRContext, Variable
from IR.IRNodes import *
from IR.IRType import IDBDatabase, IDBObjectStore
from layers.IDBContext import IDBContext
from layers.Layer import LayerType, Layer
from layers.LayerBuilder import LayerBuilder


class IDBDatabase_SchemaOps_Layer(LayerBuilder):
    name = "IDBDatabase_SchemaOps_Layer"
    layer_type = LayerType.EXECUTION

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        db_id = irctx.get_identifier_by_type(IDBDatabase)
        body = []

        # 创建一个 store
        store_name = idbctx.new_object_store_name()
        call = CallExpression(
            callee_object=db_id,
            callee_method="createObjectStore",
            args=[Literal(store_name)],
            result_name="store123"
        )

        body.append(call)

        idbctx.register_object_store(store_name)
        irctx.register_variable(Variable("store", IDBObjectStore))

        return Layer(IDBDatabase_SchemaOps_Layer.name, body, layer_type=IDBDatabase_SchemaOps_Layer.layer_type)
