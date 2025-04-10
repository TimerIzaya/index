from IR.IRContext import IRContext, Variable
from IR.IRType import IDBDatabase, IDBOpenDBRequest
from IR.IRNodes import (
    AssignmentExpression, FunctionExpression, Identifier,
    MemberExpression
)
from layers.IDBContext import IDBContext
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.IDBDatabase_Transaction_Layer import IDBDatabase_Transaction_Layer
from layers.IDBDatabase_onversionchange_Layer import IDBDatabase_onversionchange_Layer
from layers.IDBDatabase_onclose_Layer import IDBDatabase_onclose_Layer


class IDBOpenDBRequest_onsuccess_Layer(LayerBuilder):

    name = "IDBOpenDBRequest_onsuccess_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        body = []

        # 获取当前 openRequest
        open_request_id = irctx.get_identifier_by_type(IDBOpenDBRequest)

        # db = request.result
        assign_db = AssignmentExpression(
            left=Identifier("db"),
            right=MemberExpression(open_request_id, "result")
        )
        body.append(assign_db)

        # 注册 db 变量
        irctx.register_variable(Variable("db", IDBDatabase))

        # 构建 transaction 层
        txn_layer = IDBDatabase_Transaction_Layer.build(irctx, idbctx)
        body.extend(txn_layer.ir_nodes)

        # 构建 db.onversionchange 层
        version_layer = IDBDatabase_onversionchange_Layer.build(irctx, idbctx)
        body.extend(version_layer.ir_nodes)

        # 构建 db.onclose 层
        close_layer = IDBDatabase_onclose_Layer.build(irctx, idbctx)
        body.extend(close_layer.ir_nodes)

        # 构造 request.onsuccess = function(event) { ... }
        handler = AssignmentExpression(
            left=MemberExpression(open_request_id, "onsuccess"),
            right=FunctionExpression([Identifier("event")], body)
        )

        return Layer(
            IDBOpenDBRequest_onsuccess_Layer.name,
            ir_nodes=[handler],
            layer_type=IDBOpenDBRequest_onsuccess_Layer.layer_type
        )
