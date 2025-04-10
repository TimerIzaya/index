from IR.IRNodes import CallExpression, AssignmentExpression, Identifier, Literal
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder


class IDBObjectStore_DataOps_Layer(LayerBuilder):

    name = "IDBObjectStore_DataOps_Layer"
    layer_type = LayerType.EXECUTION

    @staticmethod
    def build(irctx, idbctx):
        ir_nodes = []

        # store.put(...)
        call_put = CallExpression(
            callee_object=Identifier("store"),
            callee_method="put",
            args=[Literal(True), Literal(42)],
            result_name="req_put"
        )
        ir_nodes.append(AssignmentExpression(left=Identifier("req_put"), right=call_put))

        # store.get(...)
        call_get = CallExpression(
            callee_object=Identifier("store"),
            callee_method="get",
            args=[Literal("fallback")],
            result_name="req_get"
        )
        ir_nodes.append(AssignmentExpression(left=Identifier("req_get"), right=call_get))

        # store.delete(...)
        call_del = CallExpression(
            callee_object=Identifier("store"),
            callee_method="delete",
            args=[Literal(42)],
            result_name="req_delete"
        )
        ir_nodes.append(AssignmentExpression(left=Identifier("req_delete"), right=call_del))

        return Layer(IDBObjectStore_DataOps_Layer.name, ir_nodes, layer_type=LayerType.EXECUTION)
