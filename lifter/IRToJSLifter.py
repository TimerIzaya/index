from layers.Layer import Layer, LayerType
from IR.IRNodes import *

class IRToJSLifter:
    _current_layer = None
    _visited_layers = set()

    @staticmethod
    def lift(root_layer: Layer) -> str:
        IRToJSLifter._visited_layers = set()
        return "\n".join(IRToJSLifter._convert_layer(root_layer))

    @staticmethod
    def _convert_layer(layer: Layer, indent_level: int = 0):
        IRToJSLifter._current_layer = layer
        lines = []

        for node in layer.ir_nodes:
            lines.append(IRToJSLifter._convert_node(node, indent_level))

        # 只有非 REGISTER 层的 children 才继续输出
        for child in layer.children:
            if child.name not in IRToJSLifter._visited_layers:
                lines.extend(IRToJSLifter._convert_layer(child, indent_level))

        return lines

    @staticmethod
    def _convert_node(node: IRNode, indent_level: int = 0):
        indent = "  " * indent_level

        if isinstance(node, VariableDeclaration):
            return f"{indent}{node.kind} {node.name};"

        elif isinstance(node, Identifier):
            return node.name

        elif isinstance(node, Literal):
            val = node.value
            if isinstance(val, str):
                return f"'{val}'"
            if isinstance(val, bool):
                return "true" if val else "false"
            return str(val)

        elif isinstance(node, AssignmentExpression):
            left = IRToJSLifter._convert_node(node.left, indent_level)
            right = IRToJSLifter._convert_node(node.right, indent_level)
            return f"{indent}{left} = {right};"

        elif isinstance(node, MemberExpression):
            obj = IRToJSLifter._convert_node(node.object_expr, indent_level)
            prop = node.property_name
            return f"{obj}.{prop}"

        elif isinstance(node, FunctionExpression):
            params = ", ".join(p.name for p in node.params)
            body_lines = [
                IRToJSLifter._convert_node(stmt, indent_level + 1)
                for stmt in node.body
            ]

            # 如果当前是在注册层，自动注入所有 children 的 ir_nodes
            if (
                isinstance(IRToJSLifter._current_layer, Layer)
                and IRToJSLifter._current_layer.layer_type == LayerType.REGISTER
            ):
                for child in IRToJSLifter._current_layer.children:
                    IRToJSLifter._visited_layers.add(child.name)
                    body_lines.extend(
                        IRToJSLifter._convert_layer(child, indent_level + 1)
                    )

            body = "\n".join(body_lines)
            return f"{indent}(event) => {{\n{body}\n{indent}}}"

        elif isinstance(node, CallExpression):
            callee_obj = IRToJSLifter._convert_node(node.callee_object, indent_level)
            args = ", ".join(IRToJSLifter._convert_node(arg, indent_level) for arg in node.args)
            call_expr = f"{callee_obj}.{node.callee_method}({args})"
            if node.result_name:
                return f"{indent}const {node.result_name} = {call_expr};"
            return f"{indent}{call_expr};"

        elif isinstance(node, ConsoleLog):
            msg = IRToJSLifter._convert_node(node.value, indent_level)
            return f"{indent}console.log({msg});"

        else:
            raise ValueError(f"Unsupported node type: {type(node).__name__}")
