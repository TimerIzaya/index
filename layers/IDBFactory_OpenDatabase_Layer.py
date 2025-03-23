from IR.IRNodes import CallExpression
from IR.IRParamGenerator import ParameterGenerator
from IR.IRContext import IRContext
from layers.Layer import Layer
from config import IDBFactory_OpenDatabase_Layer

def build_IDBFactory_OpenDatabase_Layer(ctx: IRContext):
    ctx.enter_layer(IDBFactory_OpenDatabase_Layer)
    gen = ParameterGenerator(ctx)
    name = gen.generate_parameter({"type": {"typename": "string"}})
    version = gen.generate_parameter({"type": {"typename": "number"}, "optional": True})
    call = CallExpression("indexedDB", "open", [name, version], result_name="openRequest")
    ctx.register_variable("openRequest", "IDBOpenDBRequest")
    return Layer(IDBFactory_OpenDatabase_Layer, ir_nodes=[call])
