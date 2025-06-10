from IR.IRContext import IRContext
from IR.IRType import IDBDatabase
from IR.layers.Globals import Global
from IR.layers.LiteralContext import LiteralContext
from IR.IRNodes import Identifier, MemberExpression, AssignmentExpression, FunctionExpression, ConsoleLog, Literal, CallExpression
from IR.layers.Layer import Layer, LayerType
from IR.layers.LayerBuilder import LayerBuilder


class IDBDatabase_onversionchange_Layer(LayerBuilder):
    name = "IDBDatabase_onversionchange_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build() -> Layer:
        db_id = Global.irctx.get_identifier_by_type(IDBDatabase)

        # 构造事件处理函数的 body
        body = [
            ConsoleLog(Literal("The version of this database has changed, release this connection")),
            CallExpression(
                callee_object=db_id,
                callee_method="close",
                args=[]
            )
        ]

        # 注册事件处理函数
        handler = AssignmentExpression(
            left=MemberExpression(db_id, "onversionchange"),
            right=FunctionExpression(
                params=[Identifier("event")],
                body=body
            )
        )

        return Layer(
            name=IDBDatabase_onversionchange_Layer.name,
            ir_nodes=[handler],
            children=[],
            layer_type=IDBDatabase_onversionchange_Layer.layer_type
        )
