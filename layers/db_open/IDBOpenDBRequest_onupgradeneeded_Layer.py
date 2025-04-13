from IR.IRContext import IRContext, Variable
from IR.IRType import IDBDatabase, IDBObjectStore, IDBOpenDBRequest
from IR.IRNodes import AssignmentExpression, FunctionExpression, Identifier, MemberExpression, CallExpression, Literal, \
    ConsoleLog
from layers.IDBContext import IDBContext
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder


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

        # 构造 db.createObjectStore(...)
        store_name = idbctx.new_object_store_name()
        create_store_call = CallExpression(
            callee_object=Identifier("db"),
            callee_method="createObjectStore",
            args=[Literal(store_name)],
            result_name="store"  # 这里就足够了
        )
        body.append(create_store_call)

        # 注册到上下文
        irctx.register_variable(Variable("store", IDBObjectStore))
        idbctx.register_object_store(store_name)

        # store.createIndex(...)
        create_index_call = CallExpression(
            callee_object=Identifier("store"),
            callee_method="createIndex",
            args=[Literal("v_index"), Literal("v_index_prop")]
        )
        body.append(create_index_call)

        # 封装为 request.onupgradeneeded = function(event) { ... }
        open_request_id = irctx.get_identifier_by_type(IDBOpenDBRequest)
        handler = AssignmentExpression(
            left=MemberExpression(open_request_id, "onupgradeneeded"),
            right=FunctionExpression([Identifier("event")], body)
        )

        return Layer(
            IDBOpenDBRequest_onupgradeneeded_Layer.name,
            ir_nodes=[handler],
            layer_type=IDBOpenDBRequest_onupgradeneeded_Layer.layer_type
        )
