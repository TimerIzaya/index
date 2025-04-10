from IR.IRContext import IRContext, Variable
from IR.IRType import IDBFactory, IDBOpenDBRequest
from IR.IRParamGenerator import ParameterGenerator
from IR.IRNodes import Identifier, Literal, CallExpression
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.IDBOpenDBRequest_onblocked_Layer import IDBOpenDBRequest_onblocked_Layer
from layers.IDBOpenDBRequest_onerror_Layer import IDBOpenDBRequest_onerror_Layer
from layers.IDBOpenDBRequest_onsuccess_Layer import IDBOpenDBRequest_onsuccess_Layer
from layers.IDBContext import IDBContext


class IDBFactory_DeleteDatabase_Layer(LayerBuilder):

    name = "IDBFactory_DeleteDatabase_Layer"
    layer_type = LayerType.CALLING

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        gen = ParameterGenerator(irctx)

        db_name = idbctx.get_database_name()
        args = [Literal(db_name)]

        call = CallExpression(
            callee_object=Identifier("indexedDB"),
            callee_method="deleteDatabase",
            args=args,
            result_name="deleteRequest"
        )
        irctx.register_variable(Variable("deleteRequest", IDBOpenDBRequest))

        # 构造子事件层
        blocked_layer = IDBOpenDBRequest_onblocked_Layer.build(irctx, idbctx)
        error_layer = IDBOpenDBRequest_onerror_Layer.build(irctx, idbctx)
        success_layer = IDBOpenDBRequest_onsuccess_Layer.build(irctx, idbctx)

        return Layer(
            IDBFactory_DeleteDatabase_Layer.name,
            ir_nodes=[call],
            children=[blocked_layer, success_layer, error_layer],
            layer_type=IDBFactory_DeleteDatabase_Layer.layer_type
        )
