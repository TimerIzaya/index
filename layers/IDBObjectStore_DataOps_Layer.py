from IR.IRNodes import CallExpression
from IR.IRParamGenerator import ParameterGenerator
from IR.IRContext import IRContext
from layers.Layer import Layer
from config import IDBObjectStore_DataOps_Layer

def build_IDBObjectStore_DataOps_Layer(ctx: IRContext):
    ctx.enter_layer(IDBObjectStore_DataOps_Layer)
    gen = ParameterGenerator(ctx)
    key = gen.generate_parameter({"type": {"typename": "string"}})
    value = gen.generate_parameter({"type": {"typename": "any"}})
    call = CallExpression("store", "put", [value, key])
    return Layer(IDBObjectStore_DataOps_Layer, ir_nodes=[call])
