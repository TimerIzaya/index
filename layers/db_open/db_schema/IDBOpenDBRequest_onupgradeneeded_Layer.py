from IR.IRContext import IRContext, Variable
from IR.IRType import IDBDatabase, IDBObjectStore, IDBOpenDBRequest
from IR.IRNodes import AssignmentExpression, FunctionExpression, Identifier, MemberExpression, CallExpression, Literal, ConsoleLog
from layers.IDBContext import IDBContext
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.db_open.db_schema.IDBDatabase_SchemaOps_Layer import IDBDatabase_SchemaOps_Layer


class IDBOpenDBRequest_onupgradeneeded_Layer(LayerBuilder):

    name = "IDBOpenDBRequest_onupgradeneeded_Layer"

    layer_type = LayerType.REGISTER

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        body = [
            ConsoleLog(Literal("db onupgraded trigered"))
        ]

        # db = event.target.result
        assign_db = AssignmentExpression(
            left=Identifier("db"),
            right=MemberExpression(
                object_expr=MemberExpression(Identifier("event"), "target"),
                property_name="result"
            )
        )
        body.append(assign_db)

        # 注册 db 到上下文
        irctx.register_variable(Variable("db", IDBDatabase))

        # ✅ 添加 schema 层
        schema_layer = IDBDatabase_SchemaOps_Layer.build(irctx, idbctx)

        # 构造事件处理器
        open_request_id = irctx.get_identifier_by_type(IDBOpenDBRequest)
        handler = AssignmentExpression(
            left=MemberExpression(open_request_id, "onupgradeneeded"),
            right=FunctionExpression([Identifier("event")], body)
        )

        return Layer(
            IDBOpenDBRequest_onupgradeneeded_Layer.name,
            ir_nodes=[handler],
            children=[schema_layer],  # ✅ 只将 schema 操作封装为子层
            layer_type=IDBOpenDBRequest_onupgradeneeded_Layer.layer_type
        )
