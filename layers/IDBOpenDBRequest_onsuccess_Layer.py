from IR.IRNodes import AssignmentExpression, FunctionExpression
from IR.IRContext import IRContext
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.IDBTransaction_ObjectStoreAccess_Layer import IDBTransaction_ObjectStoreAccess_Layer
from layers.IDBObjectStore_DataOps_Layer import IDBObjectStore_DataOps_Layer

class IDBOpenDBRequest_onsuccess_Layer(LayerBuilder):
    name = "IDBOpenDBRequest_onsuccess_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build(ctx: IRContext) -> Layer:
        ctx.enter_layer(IDBOpenDBRequest_onsuccess_Layer)

        body = []
        body.extend(IDBTransaction_ObjectStoreAccess_Layer.build(ctx).ir_nodes)
        body.extend(IDBObjectStore_DataOps_Layer.build(ctx).ir_nodes)

        func = FunctionExpression([], body)
        assign = AssignmentExpression("openRequest.onsuccess", func)

        ctx.exit_layer()
        return Layer(IDBOpenDBRequest_onsuccess_Layer.name, [assign], layer_type=IDBOpenDBRequest_onsuccess_Layer.layer_type)
