from IR.IRNodes import CallExpression
from IR.IRContext import IRContext, Variable
from IR.IRParamGenerator import ParameterGenerator
from IR.IRSchemaParser import get_parser
from IR.IRType import IDBOpenDBRequest
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.IDBOpenDBRequest_onsuccess_Layer import IDBOpenDBRequest_onsuccess_Layer


class IDBFactory_OpenDatabase_Layer(LayerBuilder):
    name = "IDBFactory_OpenDatabase_Layer"
    layer_type = LayerType.CALLING

    @staticmethod
    def build(ctx: IRContext) -> Layer:
        parser = get_parser()
        gen = ParameterGenerator(ctx)

        method = parser.getInterface("IDBFactory").getStaticMethod("open")
        args = [gen.generate_parameter(param) for param in method.getParams().raw()]

        call = CallExpression(
            callee_object=ctx.get_random_identifier("IDBFactory"),
            callee_method="open",
            args=args,
            result_name="openRequest"
        )

        ctx.register_variable(Variable("openRequest", IDBOpenDBRequest))
        onsuccess_layer = IDBOpenDBRequest_onsuccess_Layer.build(ctx)

        return Layer(IDBFactory_OpenDatabase_Layer.name, [call], children=[onsuccess_layer], layer_type=LayerType.CALLING)
