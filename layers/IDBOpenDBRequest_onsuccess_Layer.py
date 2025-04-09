from IR.IRNodes import (
    AssignmentExpression,
    MemberExpression,
    Identifier,
    FunctionExpression
)
from IR.IRContext import IRContext, Variable
from IR.IRParamGenerator import ParameterGenerator
from IR.IRType import IDBDatabase
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

        # db = request.result
        assign_db = AssignmentExpression(
            target="db",
            value=MemberExpression("request", "result")
        )
        irctx.register_variable(Variable("db", IDBDatabase))
        body.append(assign_db)

        # 构建并内联事务层
        txn_layer = IDBDatabase_Transaction_Layer.build(irctx, idbctx)
        body.extend(txn_layer.ir_nodes)

        # 注册事件处理器
        handler = AssignmentExpression(
            target="request.onsuccess",
            value=FunctionExpression(params=["event"], body=body)
        )

        return Layer(
            name=IDBOpenDBRequest_onsuccess_Layer.name,
            ir_nodes=[handler],
            children=[txn_layer],
            layer_type=IDBOpenDBRequest_onsuccess_Layer.layer_type
        )
