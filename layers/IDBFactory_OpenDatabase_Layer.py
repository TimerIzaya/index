from IR.IRNodes import CallExpression
from IR.IRParamGenerator import ParameterGenerator
from IR.IRContext import IRContext
from IR.IRSchemaParser import SchemaParser
from config import *
from layers.Layer import Layer

class IDBFactory_OpenDatabase_Layer:

    name = "IDBFactory_OpenDatabase_Layer"

    @staticmethod
    def build(ctx: IRContext) -> Layer:
        ctx.enter_layer(IDBFactory_OpenDatabase_Layer)
        gen = ParameterGenerator(ctx)

        method = SchemaParser.getInterface("IDBFactory").getStaticMethod("open")
        params = method.getParams().raw()
        # use ParameterGenerator to generator args about params

        # callee = ctx.get_random_identifier("IDBFactory")
        # call = CallExpression(callee, "open", args, result_name="openRequest")
        # ctx.register_variable("openRequest", "IDBOpenDBRequest")

        return Layer(IDBFactory_OpenDatabase_Layer.name, ir_nodes=[])
