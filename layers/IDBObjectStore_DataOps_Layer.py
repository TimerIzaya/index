from IR.IRNodes import CallExpression
from IR.IRContext import IRContext
from IR.IRParamGenerator import ParameterGenerator
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder


class IDBObjectStore_DataOps_Layer(LayerBuilder):
    name = "IDBObjectStore_DataOps_Layer"
    layer_type = LayerType.EXECUTION

    @staticmethod
    def build(ctx: IRContext) -> Layer:
        gen = ParameterGenerator(ctx)

        key = gen.generate_value_from_typename("string")
        value = gen.generate_value_from_typename("any")

        call = CallExpression(
            callee_object=ctx.get_random_identifier("IDBObjectStore"),
            callee_method="put",
            args=[value, key]
        )

        return Layer(IDBObjectStore_DataOps_Layer.name, [call], layer_type=LayerType.EXECUTION)
