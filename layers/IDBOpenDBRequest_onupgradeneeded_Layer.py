from IR.IRNodes import (
    AssignmentExpression,
    MemberExpression,
    Identifier,
    FunctionExpression,
    CallExpression
)
from IR.IRContext import IRContext, Variable
from IR.IRType import IDBDatabase, IDBObjectStore
from IR.IRParamGenerator import ParameterGenerator
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder


class IDBOpenDBRequest_onupgradeneeded_Layer(LayerBuilder):
    name = "IDBOpenDBRequest_onupgradeneeded_Layer"
    layer_type = LayerType.REGISTER

    @staticmethod
    def build(ctx: IRContext) -> Layer:
        gen = ParameterGenerator(ctx)
        body = []

        # db = event.target.result
        db_assign = AssignmentExpression(
            target="db",
            value=MemberExpression("event.target", "result")
        )
        ctx.register_variable(Variable("db", IDBDatabase))
        body.append(db_assign)

        # store = db.createObjectStore("store")
        store_name = gen.generate_value_from_typename("string")
        create_call = CallExpression(
            callee_object=Identifier("db"),
            callee_method="createObjectStore",
            args=[store_name],
            result_name="store"
        )
        ctx.register_variable(Variable("store", IDBObjectStore))
        body.append(create_call)

        handler = AssignmentExpression(
            target="request.onupgradeneeded",
            value=FunctionExpression(params=["event"], body=body)
        )

        return Layer(IDBOpenDBRequest_onupgradeneeded_Layer.name, [handler], layer_type=LayerType.REGISTER)
