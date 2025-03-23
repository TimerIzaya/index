from IR.IRNodes import CallExpression
from IR.IRParamGenerator import ParameterGenerator
from IR.IRContext import IRContext
from layers.Layer import Layer
from config import IDBTransaction_ObjectStoreAccess_Layer

def build_IDBTransaction_ObjectStoreAccess_Layer(ctx: IRContext):
    ctx.enter_layer(IDBTransaction_ObjectStoreAccess_Layer)
    gen = ParameterGenerator(ctx)
    store_name = gen.generate_parameter({"type": {"typename": "string"}})
    call = CallExpression("txn", "objectStore", [store_name], result_name="store")
    ctx.register_variable("store", "IDBObjectStore")
    return Layer(IDBTransaction_ObjectStoreAccess_Layer, ir_nodes=[call])
