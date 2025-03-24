from IR.IRNodes import CallExpression
from IR.IRContext import IRContext, Variable
from IR.IRParamGenerator import ParameterGenerator
from IR.IRSchemaParser import get_parser
from IR.IRType import IDBOpenDBRequest
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder


# req = windows.indexDB.open("databasename", 5)
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
        return Layer(IDBFactory_OpenDatabase_Layer.name, [call], layer_type=IDBFactory_OpenDatabase_Layer.layer_type)
