from IR.layers.Layer import Layer, LayerType
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
        stmts = layer.ir_nodes
        i = 0

        while i < len(stmts):
            stmt = stmts[i]

            # 合并声明 + 赋值
            if (
                i + 1 < len(stmts)
                and isinstance(stmt, VariableDeclaration)
                and isinstance(stmts[i + 1], AssignmentExpression)
                and isinstance(stmts[i + 1].left, Identifier)
                and stmts[i + 1].left.name == stmt.name
            ):
                rhs = IRToJSLifter._convert_node(stmts[i + 1].right, 0)
                if rhs.endswith(";"):
                    rhs = rhs[:-1]
                line = f"{'  ' * indent_level}{stmt.kind} {stmt.name} = {rhs};"
                lines.append(line)
                i += 2
                continue

            lines.append(IRToJSLifter._convert_node(stmt, indent_level))
            i += 1

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
            if isinstance(val, dict):
                js_items = [
                    f"'{k}': {IRToJSLifter._convert_node(Literal(v), 0)}"
                    for k, v in val.items()
                ]
                return "{" + ", ".join(js_items) + "}"
            if isinstance(val, list):
                js_items = [IRToJSLifter._convert_node(Literal(v), 0) for v in val]
                return "[" + ", ".join(js_items) + "]"
            return str(val)

        elif isinstance(node, AssignmentExpression):
            left = IRToJSLifter._convert_node(node.left, indent_level)
            right = IRToJSLifter._convert_node(node.right, 0)
            if right.endswith(";"):
                right = right.rstrip(";")
            return f"{indent}{left} = {right};"

        elif isinstance(node, MemberExpression):
            obj = IRToJSLifter._convert_node(node.object_expr, indent_level)
            return f"{obj}.{node.property_name}"

        elif isinstance(node, FunctionExpression):
            params = ", ".join(p.name for p in node.params)
            body_lines = [
                IRToJSLifter._convert_node(stmt, indent_level + 1)
                for stmt in node.body
            ]

            if (
                isinstance(IRToJSLifter._current_layer, Layer)
                and IRToJSLifter._current_layer.layer_type == LayerType.REGISTER
            ):
                for child in IRToJSLifter._current_layer.children:
                    IRToJSLifter._visited_layers.add(child.name)
                    body_lines.extend(
                        IRToJSLifter._convert_layer(child, indent_level + 1)
                    )

            indented_body = "\n".join("  " * (indent_level + 1) + line.lstrip() for line in body_lines)
            return f"{indent}(event) => {{\n{indented_body}\n{indent}}}"

        elif isinstance(node, CallExpression):
            callee_obj = IRToJSLifter._convert_node(node.callee_object, indent_level)
            args = ", ".join(IRToJSLifter._convert_node(arg, indent_level) for arg in node.args)
            call_expr = f"{callee_obj}.{node.callee_method}({args})"
            if node.result_name:
                return f"{indent}const {node.result_name} = {call_expr}"
            return f"{indent}{call_expr}"

        elif isinstance(node, ConsoleLog):
            msg = IRToJSLifter._convert_node(node.value, indent_level)
            return f"{indent}console.log({msg});"

        else:
            raise ValueError(f"Unsupported node type: {type(node).__name__}")
