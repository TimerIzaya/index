from IR.IRNodes import AssignmentExpression, FunctionExpression, CallExpression, Identifier, Literal
from IR.IRContext import IRContext, Variable
from layers.IDBContext import IDBContext
from IR.IRParamGenerator import ParameterGenerator
from IR.IRType import IDBObjectStore, IDBDatabase
from IR.IRSchemaParser import get_parser
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder


class IDBOpenDBRequest_onupgradeneeded_Layer(LayerBuilder):
    name = "IDBOpenDBRequest_onupgradeneeded_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        parser = get_parser()
        gen = ParameterGenerator(irctx)

        # db = event.target.result
        assign_db = AssignmentExpression(
            target="db",
            value=CallExpression(Identifier("event.target"), "result", [])
        )
        irctx.register_variable(Variable("db", IDBDatabase))

        # 创建 objectStore
        create_store_method = parser.getInterface("IDBDatabase").getInstanceMethod("createObjectStore")
        store_args = [arg for p in create_store_method.getParams().raw() if (arg := gen.generate_parameter(p)) is not None]
        store_name = store_args[0].value if isinstance(store_args[0], Literal) else "store"

        idbctx.register_object_store(store_name)

        create_store_call = CallExpression(
            callee_object=Identifier("db"),
            callee_method="createObjectStore",
            args=store_args,
            result_name="store"
        )
        irctx.register_variable(Variable("store", IDBObjectStore))

        # 创建 index
        create_index_method = parser.getInterface("IDBObjectStore").getInstanceMethod("createIndex")
        index_args = [arg for p in create_index_method.getParams().raw() if (arg := gen.generate_parameter(p)) is not None]
        create_index_call = CallExpression(
            callee_object=Identifier("store"),
            callee_method="createIndex",
            args=index_args
        )

        if index_args and isinstance(index_args[0], Literal):
            idbctx.register_index(store_name, index_args[0].value)

        handler_body = [assign_db, create_store_call, create_index_call]


        handler = AssignmentExpression(
            target="openRequest.onupgradeneeded",
            value=FunctionExpression(params=["event"], body=handler_body)
        )

        return Layer(
            name=IDBOpenDBRequest_onupgradeneeded_Layer.name,
            ir_nodes=[handler],
            layer_type=IDBOpenDBRequest_onupgradeneeded_Layer.layer_type
        )
