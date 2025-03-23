from IR.IRNodes import AssignmentExpression, FunctionExpression
from IR.IRContext import IRContext
from layers.Layer import Layer
from config import IDBOpenDBRequest_onsuccess_Layer
from layers.IDBTransaction_ObjectStoreAccess_Layer import build_IDBTransaction_ObjectStoreAccess_Layer
from layers.IDBObjectStore_DataOps_Layer import build_IDBObjectStore_DataOps_Layer


def build_IDBOpenDBRequest_onsuccess_Layer(ctx: IRContext):
    ctx.enter_layer(IDBOpenDBRequest_onsuccess_Layer)

    body = []
    body.append(build_IDBTransaction_ObjectStoreAccess_Layer(ctx).ir_nodes[0])
    body.append(build_IDBObjectStore_DataOps_Layer(ctx).ir_nodes[0])

    assign = AssignmentExpression("openRequest.onsuccess", FunctionExpression([], body))
    ctx.exit_layer()

    return Layer(IDBOpenDBRequest_onsuccess_Layer, ir_nodes=[assign])
