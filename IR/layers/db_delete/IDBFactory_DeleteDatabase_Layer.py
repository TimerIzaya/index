from IR.IRContext import IRContext, Variable
from IR.IRType import IDBOpenDBRequest
from IR.IRParamValueGenerator import IRParamValueGenerator
from IR.IRNodes import Identifier, Literal, CallExpression
from IR.layers.Globals import Global
from IR.layers.Layer import Layer, LayerType
from IR.layers.LayerBuilder import LayerBuilder
from IR.layers.IDBContext import IDBContext
from IR.layers.db_delete.IDBDeleteDBRequest_onblocked_Layer import IDBDeleteDBRequest_onblocked_Layer
from IR.layers.db_delete.IDBDeleteDBRequest_onerror_Layer import IDBDeleteDBRequest_onerror_Layer
from IR.layers.db_delete.IDBDeteleDBRequest_onsuccess_Layer import IDBDeleteDBRequest_onsuccess_Layer


class IDBFactory_DeleteDatabase_Layer(LayerBuilder):

    name = "IDBFactory_DeleteDatabase_Layer"
    layer_type = LayerType.CALLING

    @staticmethod
    def build() -> Layer:
        gen = IRParamValueGenerator(Global.irctx)

        db_name = Global.idbctx.get_database_name()
        args = [Literal(db_name)]

        call = CallExpression(
            callee_object=Identifier("indexedDB"),
            callee_method="deleteDatabase",
            args=args,
            result_name="deleteRequest"
        )
        Global.irctx.register_variable(Variable("deleteRequest", IDBOpenDBRequest))

        # 构造子事件层
        blocked_layer = IDBDeleteDBRequest_onblocked_Layer.build()
        error_layer = IDBDeleteDBRequest_onerror_Layer.build()
        success_layer = IDBDeleteDBRequest_onsuccess_Layer.build()

        return Layer(
            IDBFactory_DeleteDatabase_Layer.name,
            ir_nodes=[call],
            children=[blocked_layer, success_layer, error_layer],
            layer_type=IDBFactory_DeleteDatabase_Layer.layer_type
        )
