from IR.IRContext import IRContext
from IR.IRNodes import CallExpression, AssignmentExpression, Identifier, Literal
from IR.IRType import IDBObjectStore
from layers.IDBContext import IDBContext
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder


class IDBObjectStore_DataOps_Layer(LayerBuilder):
    name = "IDBObjectStore_DataOps_Layer"
    layer_type = LayerType.EXECUTION

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        store_id = irctx.get_identifier_by_type(IDBObjectStore)
        body = []

        body.append(CallExpression(store_id, "put", [Literal(True), Literal(42)], result_name="req_put"))
        body.append(CallExpression(store_id, "get", [Literal("fallback")], result_name="req_get"))
        # body.append(CallExpression(store_id, "delete", [Literal(42)], result_name="req_delete"))

        return Layer(IDBObjectStore_DataOps_Layer.name, body, layer_type=IDBObjectStore_DataOps_Layer.layer_type)
