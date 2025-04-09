from IR.IRNodes import CallExpression
from IR.IRContext import IRContext, Variable
from IR.IRType import IDBObjectStore
from IR.IRParamGenerator import ParameterGenerator
from IR.IRSchemaParser import get_parser
from layers.IDBContext import IDBContext
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.IDBObjectStore_DataOps_Layer import IDBObjectStore_DataOps_Layer


class IDBTransaction_ObjectStoreAccess_Layer(LayerBuilder):
    name = "IDBTransaction_ObjectStoreAccess_Layer"
    layer_type = LayerType.ACCESS

    @staticmethod
    def build(ctx: IRContext, idb: IDBContext) -> Layer:
        parser = get_parser()
        method = parser.getInterface("IDBTransaction").getInstanceMethod("objectStore")
        gen = ParameterGenerator(ctx)

        store_args = [arg for p in method.getParams().raw() if (arg := gen.generate_parameter(p)) is not None]
        call = CallExpression(
            callee_object=ctx.get_random_identifier("IDBTransaction"),
            callee_method="objectStore",
            args=store_args,
            result_name="store"
        )

        ctx.register_variable(Variable("store", IDBObjectStore))

        child = IDBObjectStore_DataOps_Layer.build(ctx, idb)

        return Layer(
            name=IDBTransaction_ObjectStoreAccess_Layer.name,
            ir_nodes=[call],
            children=[child],
            layer_type=IDBTransaction_ObjectStoreAccess_Layer.layer_type
        )
