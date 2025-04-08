import json
from IR.IRNodes import (
    Program, Identifier, Literal, MemberExpression,
    CallExpression, AssignmentExpression, FunctionExpression
)
from layers.Layer import Layer

class IRToJSConverter:
    def __init__(self, indent="  "):
        self.indent = indent
        self.level = 0

    def convert_program(self, program: Program) -> str:
        return self._convert_layers(program.layers)

    def _convert_layers(self, layers) -> str:
        code = ""
        for layer in layers:
            code += self._convert_layer(layer)
        return code

    def _convert_layer(self, layer: Layer) -> str:
        ir_code = "\n".join(self._convert_node(n) for n in layer.ir_nodes)
        child_code = self._convert_layers(layer.children)
        return f"{ir_code}\n{child_code}"

    def _convert_node(self, node) -> str:
        if isinstance(node, CallExpression):
            args = ", ".join(self._convert_node(arg) for arg in node.args)
            code = f"{self._convert_node(node.callee_object)}.{node.callee_method}({args})"
            if node.result_name:
                code = f"const {node.result_name} = {code}"
            return self._indent(code)

        elif isinstance(node, AssignmentExpression):
            return self._indent(f"{node.target} = {self._convert_node(node.value)}")

        elif isinstance(node, MemberExpression):
            return f"{node.object_name}.{node.property_name}"

        elif isinstance(node, Identifier):
            return node.name

        elif isinstance(node, Literal):
            return json.dumps(node.value)

        elif isinstance(node, FunctionExpression):
            params = ", ".join(node.params)
            self.level += 1
            body = "\n".join(self._convert_node(n) for n in node.body)
            self.level -= 1
            return self._indent(f"(event) => {{\n{body}\n{self._indent('}}')}")

        else:
            return self._indent(f"// [Unknown node: {type(node).__name__}]")

    def _indent(self, line: str) -> str:
        return f"{self.indent * self.level}{line}"


# === ✅ MAIN 测试入口 ===
if __name__ == "__main__":
    import json
    from pathlib import Path

    # 加载 IR JSON 文件
    input_path = Path("IRDemo.json")
    with open(input_path, "r") as f:
        ir_data = json.load(f)

    # 用于测试的 Program.from_dict (假设结构直接传递给 Program)
    program = Program.from_dict(ir_data)

    # 转换为 JS 源码
    converter = IRToJSConverter()
    js_code = converter.convert_program(program)

    # 输出
    print(js_code)
