from IR.IRContext import IRContext, Variable
from IR.IRType import IDBDatabase, IDBOpenDBRequest
from IR.IRNodes import (
    AssignmentExpression, FunctionExpression, Identifier,
    MemberExpression, Literal, CallExpression
)
from IR.layers.Globals import Global
from IR.layers.LiteralContext import LiteralContext
from IR.layers.Layer import Layer, LayerType
from IR.layers.LayerBuilder import LayerBuilder
from IR.layers.db_transaction.IDBDatabase_Transaction_Layer import IDBDatabase_Transaction_Layer
from IR.layers.db_open.IDBDatabase_onversionchange_Layer import IDBDatabase_onversionchange_Layer
from IR.layers.db_open.IDBDatabase_onclose_Layer import IDBDatabase_onclose_Layer


class IDBOpenDBRequest_onsuccess_Layer(LayerBuilder):

    name = "IDBOpenDBRequest_onsuccess_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build() -> Layer:
        body = [
            CallExpression(Identifier("console"), "log", [Literal("db onsuccess triggered")])
        ]

        children = []

        # 获取当前 openRequest
        open_request_id = Global.irctx.get_identifier_by_type(IDBOpenDBRequest)

        # db = request.result
        assign_db = AssignmentExpression(
            left=Identifier("db"),
            right=MemberExpression(open_request_id, "result")
        )
        body.append(assign_db)

        # 注册 db 变量
        Global.irctx.register_variable(Variable("db", IDBDatabase))

        # 构建 transaction 层
        txn_layer = IDBDatabase_Transaction_Layer.build()
        children.append(txn_layer)

        # 构建 db.onversionchange 层
        version_layer = IDBDatabase_onversionchange_Layer.build()
        children.append(version_layer)

        # 构建 db.onclose 层
        close_layer = IDBDatabase_onclose_Layer.build()
        children.append(close_layer)

        # 构造 request.onsuccess = function(event) { ... }
        handler = AssignmentExpression(
            left=MemberExpression(open_request_id, "onsuccess"),
            right=FunctionExpression([Identifier("event")], body)
        )

        return Layer(
            name=IDBOpenDBRequest_onsuccess_Layer.name,
            ir_nodes=[handler],
            children=children,
            layer_type=IDBOpenDBRequest_onsuccess_Layer.layer_type
        )
