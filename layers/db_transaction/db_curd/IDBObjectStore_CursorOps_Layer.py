from IR.IRContext import IRContext
from IR.IRNodes import CallExpression
from IR.IRType import IDBObjectStore
from layers.IDBContext import IDBContext
from layers.Layer import LayerType, Layer
from layers.LayerBuilder import LayerBuilder


class IDBObjectStore_CursorOps_Layer(LayerBuilder):
    name = "IDBObjectStore_CursorOps_Layer"
    layer_type = LayerType.EXECUTION

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        store_id = irctx.get_identifier_by_type(IDBObjectStore)
        body = []

        call = CallExpression(
            callee_object=store_id,
            callee_method="openCursor",
            args=[],
            result_name="cursorRequest"
        )
        body.append(call)

        return Layer(IDBObjectStore_CursorOps_Layer.name, body, layer_type=IDBObjectStore_CursorOps_Layer.layer_type)
