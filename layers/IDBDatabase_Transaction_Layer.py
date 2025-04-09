from IR.IRNodes import CallExpression
from IR.IRContext import IRContext, Variable
from IR.IRParamGenerator import ParameterGenerator
from IR.IRType import IDBTransaction
from IR.IRSchemaParser import get_parser
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.IDBTransaction_ObjectStoreAccess_Layer import IDBTransaction_ObjectStoreAccess_Layer


class IDBDatabase_Transaction_Layer(LayerBuilder):
    name = "IDBDatabase_Transaction_Layer"
    layer_type = LayerType.CALLING

    @staticmethod
    def build(ctx: IRContext) -> Layer:
        parser = get_parser()
        method = parser.getInterface("IDBDatabase").getInstanceMethod("transaction")
        gen = ParameterGenerator(ctx)

        # 动态构造参数
        params = method.getParams().raw()
        args = [arg for p in params if (arg := gen.generate_parameter(p)) is not None]

        call = CallExpression(
            callee_object=ctx.get_random_identifier("IDBDatabase"),
            callee_method="transaction",
            args=args,
            result_name="txn"
        )

        ctx.register_variable(Variable("txn", IDBTransaction))

        # ✅ 接入子操作层
        ir_nodes = [call]
        access_nodes = IDBTransaction_ObjectStoreAccess_Layer.build_body(ctx)
        ir_nodes.extend(access_nodes)

        return Layer(
            IDBDatabase_Transaction_Layer.name,
            ir_nodes,
            layer_type=IDBDatabase_Transaction_Layer.layer_type
        )
