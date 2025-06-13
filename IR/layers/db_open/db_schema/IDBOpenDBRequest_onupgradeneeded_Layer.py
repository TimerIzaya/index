from IR.IRContext import IRContext, Variable
from IR.IRNodes import AssignmentExpression, FunctionExpression, Identifier, MemberExpression, CallExpression, Literal, ConsoleLog
from IR.layers.Globals import Global
from IR.layers.LiteralContext import LiteralContext
from IR.layers.Layer import Layer, LayerType
from IR.layers.LayerBuilder import LayerBuilder
from IR.layers.db_open.db_schema.IDBDatabase_SchemaOps_Layer import IDBDatabase_SchemaOps_Layer
from IR.type.IDBType import IDBType


class IDBOpenDBRequest_onupgradeneeded_Layer(LayerBuilder):

    name = "IDBOpenDBRequest_onupgradeneeded_Layer"

    layer_type = LayerType.REGISTER

    @staticmethod
    def build() -> Layer:
        Global.irctx.enter_layer(IDBOpenDBRequest_onupgradeneeded_Layer)
        body = [
            ConsoleLog(Literal("db onupgraded trigered"))
        ]

        # db = event.target.result
        assign_db = AssignmentExpression(
            left=Identifier("db"),
            right=MemberExpression(
                objectExpr=MemberExpression(Identifier("event"), "target"),
                property_name="result"
            )
        )
        body.append(assign_db)

        # 注册 db 到上下文
        Global.irctx.register_variable(Variable("db", IDBType.IDBDatabase))

        # ✅ 添加 schema 层
        schema_layer = IDBDatabase_SchemaOps_Layer.build()

        # 构造事件处理器
        open_request_id = Global.irctx.get_identifier_by_type(IDBType.IDBOpenDBRequest)
        handler = AssignmentExpression(
            left=MemberExpression(open_request_id, "onupgradeneeded"),
            right=FunctionExpression([Identifier("event")], body)
        )

        Global.irctx.exit_layer()
        return Layer(
            IDBOpenDBRequest_onupgradeneeded_Layer.name,
            ir_nodes=[handler],
            children=[schema_layer],  # ✅ 只将 schema 操作封装为子层
            layer_type=IDBOpenDBRequest_onupgradeneeded_Layer.layer_type
        )
