from IR.IRNodes import CallExpression
from IR.IRContext import IRContext, Variable
from IR.IRParamGenerator import ParameterGenerator
from IR.IRType import IDBObjectStore
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder

class IDBTransaction_ObjectStoreAccess_Layer(LayerBuilder):
    name = "IDBTransaction_ObjectStoreAccess_Layer"
    layer_type = LayerType.ACCESS

    @staticmethod
    def build(ctx: IRContext) -> Layer:
        gen = ParameterGenerator(ctx)
        store_name = gen.generate_parameter_from_typename("string")

        call = CallExpression(
            callee_object=ctx.get_random_identifier("IDBTransaction"),
            callee_method="objectStore",
            args=[store_name],
            result_name="store"
        )

        ctx.register_variable(Variable("store", IDBObjectStore))
        return Layer(IDBTransaction_ObjectStoreAccess_Layer.name, [call], layer_type=IDBTransaction_ObjectStoreAccess_Layer.layer_type)
