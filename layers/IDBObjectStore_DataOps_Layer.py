from IR.IRNodes import CallExpression, Identifier
from IR.IRContext import IRContext, Variable
from IR.IRType import IDBRequest
from IR.IRParamGenerator import ParameterGenerator


class IDBObjectStore_DataOps_Layer:
    @staticmethod
    def build_body(ctx: IRContext):
        gen = ParameterGenerator(ctx)
        body = []

        # store.get(...)
        get_key = gen.generate_value_from_typename("any")
        get_call = CallExpression(
            callee_object=Identifier("store"),
            callee_method="get",
            args=[get_key],
            result_name="req_get"
        )
        ctx.register_variable(Variable("req_get", IDBRequest))
        body.append(get_call)

        # store.delete(...)
        del_key = gen.generate_value_from_typename("any")
        del_call = CallExpression(
            callee_object=Identifier("store"),
            callee_method="delete",
            args=[del_key],
            result_name="req_del"
        )
        ctx.register_variable(Variable("req_del", IDBRequest))
        body.append(del_call)

        return body
