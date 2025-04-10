import json
from IR.IRNodes import (
    VariableDeclaration,
    AssignmentExpression,
    MemberExpression,
    FunctionExpression,
    CallExpression,
    Identifier,
    Literal,
)
from layers.Layer import Layer

class IRToJSLifter:
    @staticmethod
    def _convert_layer(layer: Layer):
        lines = []
        for node in layer.ir_nodes:
            lines.append(IRToJSLifter._convert_node(node))
        for child in layer.children:
            lines.extend(IRToJSLifter._convert_layer(child))
        return lines

    @staticmethod
    def _convert_node(node):
        if isinstance(node, VariableDeclaration):
            return f"{node.kind} {node.name};"

        if isinstance(node, AssignmentExpression):
            left = IRToJSLifter._convert_node(node.left)
            right = IRToJSLifter._convert_node(node.right)
            return f"{left} = {right};"

        if isinstance(node, MemberExpression):
            object_expr = IRToJSLifter._convert_node(node.object_expr)
            prop_name = node.property_name if isinstance(node.property_name, str) else IRToJSLifter._convert_node(node.property_name)
            return f"{object_expr}.{prop_name}"

        if isinstance(node, FunctionExpression):
            body = "\n  ".join(IRToJSLifter._convert_node(stmt) for stmt in node.body)
            return f"(event) => {{\n  {body}\n}}"

        if isinstance(node, CallExpression):
            args = ", ".join(
                IRToJSLifter._convert_node(arg)
                for arg in node.args
                if not (isinstance(arg, Literal) and arg.value == "OPTIONAL_JUMP")
            )
            call = f"{IRToJSLifter._convert_node(node.callee_object)}.{node.callee_method}({args})"
            return f"const {node.result_name} = {call};" if node.result_name else f"{call};"

        if isinstance(node, Identifier):
            return node.name

        if isinstance(node, Literal):
            return json.dumps(node.value)

        raise ValueError(f"Unsupported node type: {type(node).__name__}")

