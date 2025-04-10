from IR.IRContext import IRContext, Variable
from IR.IRType import IDBDatabase, IDBOpenDBRequest
from IR.IRNodes import AssignmentExpression, FunctionExpression, Identifier, MemberExpression
from layers.IDBContext import IDBContext
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.IDBDatabase_Transaction_Layer import IDBDatabase_Transaction_Layer


class IDBOpenDBRequest_onsuccess_Layer(LayerBuilder):

    name = "IDBOpenDBRequest_onsuccess_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        body = []
        open_request_id = irctx.get_identifier_by_type(IDBOpenDBRequest)

        # db = request.result
        assign_db = AssignmentExpression(
            left=Identifier("db"),
            right=MemberExpression(open_request_id, "result")
        )
        body.append(assign_db)

        # 注册变量
        irctx.register_variable(Variable("db", IDBDatabase))

        # 构建 transaction 层
        txn_layer = IDBDatabase_Transaction_Layer.build(irctx, idbctx)
        body.extend(txn_layer.ir_nodes)

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
