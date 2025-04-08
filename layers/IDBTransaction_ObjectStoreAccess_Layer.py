from IR.IRNodes import CallExpression, Identifier
from IR.IRContext import IRContext, Variable
from IR.IRType import IDBObjectStore, IDBRequest
from IR.IRParamGenerator import ParameterGenerator
from layers.IDBObjectStore_DataOps_Layer import IDBObjectStore_DataOps_Layer


class IDBTransaction_ObjectStoreAccess_Layer:
    @staticmethod
    def build_body(ctx: IRContext):
        gen = ParameterGenerator(ctx)
        body = []

        # store = txn.objectStore("store")
        store_name = gen.generate_value_from_typename("string")
        store_call = CallExpression(
            callee_object=Identifier("txn"),
            callee_method="objectStore",
            args=[store_name],
            result_name="store"
        )
        ctx.register_variable(Variable("store", IDBObjectStore))
        body.append(store_call)

        # store.put(...)
        value = gen.generate_value_from_typename("any")
        key = gen.generate_value_from_typename("any")
        put_call = CallExpression(
            callee_object=Identifier("store"),
            callee_method="put",
            args=[value, key],
            result_name="req_put"
        )
        ctx.register_variable(Variable("req_put", IDBRequest))
        body.append(put_call)

        # 🔗 插入 store.get / delete 等 IR
        body.extend(IDBObjectStore_DataOps_Layer.build_body(ctx))

        return body
