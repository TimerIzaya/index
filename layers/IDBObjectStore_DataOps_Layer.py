from IR.IRNodes import CallExpression
from IR.IRContext import IRContext
from IR.IRParamGenerator import ParameterGenerator
from IR.IRSchemaParser import get_parser
from layers.IDBContext import IDBContext
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder


class IDBObjectStore_DataOps_Layer(LayerBuilder):
    name = "IDBObjectStore_DataOps_Layer"
    layer_type = LayerType.EXECUTION

    @staticmethod
    def build(ctx: IRContext, idb: IDBContext) -> Layer:
        parser = get_parser()
        gen = ParameterGenerator(ctx)

        store = ctx.get_random_identifier("IDBObjectStore")
        if not store:
            return Layer(IDBObjectStore_DataOps_Layer.name, [])

        ops = []
        for method_name in ["put", "get", "delete"]:
            method = parser.getInterface("IDBObjectStore").getInstanceMethod(method_name)
            params = method.getParams().raw()
            args = [arg for p in params if (arg := gen.generate_parameter(p)) is not None]
            call = CallExpression(
                callee_object=store,
                callee_method=method_name,
                args=args,
                result_name=f"req_{method_name}"
            )
            ops.append(call)

        return Layer(
            IDBObjectStore_DataOps_Layer.name,
            ir_nodes=ops,
            layer_type=IDBObjectStore_DataOps_Layer.layer_type
        )
