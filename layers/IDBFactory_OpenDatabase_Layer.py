from IR.IRNodes import CallExpression
from IR.IRContext import IRContext, Variable
from IR.IRType import IDBFactory, IDBOpenDBRequest
from IR.IRParamGenerator import ParameterGenerator
from IR.IRSchemaParser import get_parser
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder

# 子层导入
from layers.IDBOpenDBRequest_onupgradeneeded_Layer import IDBOpenDBRequest_onupgradeneeded_Layer
from layers.IDBOpenDBRequest_onsuccess_Layer import IDBOpenDBRequest_onsuccess_Layer
from layers.IDBOpenDBRequest_onerror_Layer import IDBOpenDBRequest_onerror_Layer
from layers.IDBOpenDBRequest_onblocked_Layer import IDBOpenDBRequest_onblocked_Layer


class IDBFactory_OpenDatabase_Layer(LayerBuilder):
    name = "IDBFactory_OpenDatabase_Layer"
    layer_type = LayerType.CALLING

    @staticmethod
    def build(ctx: IRContext) -> Layer:
        parser = get_parser()
        method = parser.getInterface("IDBFactory").getStaticMethod("open")
        gen = ParameterGenerator(ctx)

        args = [gen.generate_parameter(param) for param in method.getParams().raw()]
        callee = ctx.get_random_identifier("IDBFactory")

        call = CallExpression(
            callee_object=callee,
            callee_method="open",
            args=args,
            result_name="request"
        )

        # 注册 openRequest 变量
        ctx.register_variable(Variable("request", IDBOpenDBRequest))

        # 构造子层
        upgrade_layer = IDBOpenDBRequest_onupgradeneeded_Layer.build(ctx)
        success_layer = IDBOpenDBRequest_onsuccess_Layer.build(ctx)
        error_layer = IDBOpenDBRequest_onerror_Layer.build(ctx)
        blocked_layer = IDBOpenDBRequest_onblocked_Layer.build(ctx)

        return Layer(
            IDBFactory_OpenDatabase_Layer.name,
            [call],
            children=[
                upgrade_layer,
                success_layer,
                error_layer,
                blocked_layer
            ],
            layer_type=LayerType.CALLING
        )
