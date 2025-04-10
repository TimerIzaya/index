import json
from layers.Layer import Layer


class IRToJSLifter:
    @staticmethod
    def convert(layer: Layer, indent_level=0) -> str:
        lines = IRToJSLifter._convert_layer(layer, indent_level)
        return "\n".join(lines)

    @staticmethod
    def _convert_layer(layer: Layer, indent_level=0) -> list[str]:
        lines = []
        for node in layer.ir_nodes:
            lines.append(IRToJSLifter._convert_node(node, indent_level))
        for child in layer.children:
            lines.extend(IRToJSLifter._convert_layer(child, indent_level))
        return lines

    @staticmethod
    def _convert_node(node, indent_level: int) -> str:
        if isinstance(node, str):
            return "  " * indent_level + node

        if node.__class__.__name__ == "VariableDeclaration":
            return f"{'  ' * indent_level}{node.kind} {node.name};"

        elif node.__class__.__name__ == "AssignmentExpression":
            left = IRToJSLifter._convert_node(node.left, 0)
            right = IRToJSLifter._convert_node(node.right, indent_level)
            return f"{'  ' * indent_level}{left} = {right};"

        elif node.__class__.__name__ == "Identifier":
            return node.name

        elif node.__class__.__name__ == "Literal":
            return json.dumps(node.value)

        elif node.__class__.__name__ == "MemberExpression":
            return f"{IRToJSLifter._convert_node(node.object_expr, indent_level)}.{node.property_name}"

        elif node.__class__.__name__ == "FunctionExpression":
            params = ", ".join(p.name for p in node.params)
            body_lines = [
                IRToJSLifter._convert_node(stmt, indent_level + 1)
                for stmt in node.body
            ]
            body = "\n".join(body_lines)
            return f"({params}) => {{\n{body}\n{'  ' * indent_level}}}"

        elif node.__class__.__name__ == "CallExpression":
            args = ", ".join(IRToJSLifter._convert_node(arg, indent_level) for arg in node.args)
            call_str = f"{IRToJSLifter._convert_node(node.callee_object, indent_level)}.{node.callee_method}({args})"
            if node.result_name:
                return f"{'  ' * indent_level}const {node.result_name} = {call_str};"
            else:
                return f"{'  ' * indent_level}{call_str};"

        elif node.__class__.__name__ == "ConsoleLog":
            val = IRToJSLifter._convert_node(node.value, indent_level)
            return f"{'  ' * indent_level}console.log({val});"

        else:
            raise ValueError(f"Unsupported node type: {type(node).__name__}")


if __name__ == "__main__":
    from layers.Layer import Layer
    import sys

    with open("IRDemo.json", "r", encoding="utf-8") as f:
        ir_data = json.load(f)
        root_layer = Layer.from_dict(ir_data)
        lifted_code = IRToJSLifter.convert(root_layer)
        print(lifted_code)
