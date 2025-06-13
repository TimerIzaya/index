from IR.layers.Globals import Global
from IR.type.IDBType import IDBType
from schema.IDBSchemaParser import IDBSchemaParser
from IR.IRNodes import CallExpression, Identifier, Literal
from IR.IRContext import IRContext, Variable
from config import FATHER
from IR.layers.LiteralContext import LiteralContext
from IR.IRParamValueGenerator import IRParamValueGenerator
from IR.layers.db_open.IDBOpenDBRequest_onblocked_Layer import IDBOpenDBRequest_onblocked_Layer
from IR.layers.db_open.IDBOpenDBRequest_onerror_Layer import IDBOpenDBRequest_onerror_Layer
from IR.layers.db_open.db_schema.IDBOpenDBRequest_onupgradeneeded_Layer import IDBOpenDBRequest_onupgradeneeded_Layer
from IR.layers.db_open.IDBOpenDBRequest_onsuccess_Layer import IDBOpenDBRequest_onsuccess_Layer
from IR.layers.Layer import Layer, LayerType
from IR.layers.LayerBuilder import LayerBuilder


class IDBFactory_OpenDatabase_Layer(LayerBuilder):
    name = "IDBFactory_OpenDatabase_Layer"
    layer_type = LayerType.CALLING

    @staticmethod
    def build() -> Layer:
        parser = IDBSchemaParser()
        method = parser.getInterface("IDBFactory").getStaticMethod("open")

        # 单独生成 name/version 参数，便于注册数据库
        open_params = method.getParams().raw()
        name_param = IRParamValueGenerator.generateValueByParamInfo(open_params[0])  # string
        version_param = IRParamValueGenerator.generateValueByParamInfo(open_params[1])  # number?

        # 注册数据库名
        if isinstance(name_param, Literal):
            Global.itctx.start_database(name_param.value)

        args = [name_param, version_param]

        call = CallExpression(
            callee_object=Identifier(FATHER),
            callee_method="open",
            args=args,
            result_name="openRequest"
        )

        # 注册 indexedDB 对象
        Global.irctx.register_variable(Variable("FATHER", IDBType.IDBFactory))

        Global.irctx.register_variable(Variable("openRequest", IDBType.IDBOpenDBRequest))

        # 注册子事件层
        upgrade_layer = IDBOpenDBRequest_onupgradeneeded_Layer.build()
        success_layer = IDBOpenDBRequest_onsuccess_Layer.build()
        blocked_layer = IDBOpenDBRequest_onblocked_Layer.build()
        error_layer = IDBOpenDBRequest_onerror_Layer.build()

        return Layer(
            name=IDBFactory_OpenDatabase_Layer.name,
            ir_nodes=[call],
            children=[upgrade_layer, success_layer, blocked_layer, error_layer],
            layer_type=IDBFactory_OpenDatabase_Layer.layer_type
        )
