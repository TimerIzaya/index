import json
from IR.IRNodes import IRNodeFactory, Program


class IRToJSLifter:
    @staticmethod
    def lift_program(program: Program) -> str:
        d = program.to_dict()
        IRToJSLifter._inject_variable_declarations(d)

        js_lines = []
        for layer in d["layers"]:
            js_lines.extend(IRToJSLifter._convert_layer(layer))
        return "\n".join(js_lines)

    @staticmethod
    def _inject_variable_declarations(prog_dict: dict):
        used = set()

        def collect_identifiers(node):
            if isinstance(node, dict):
                if node.get("type") == "Identifier":
                    used.add(node["name"])
                for v in node.values():
                    collect_identifiers(v)
            elif isinstance(node, list):
                for item in node:
                    collect_identifiers(item)

        for layer in prog_dict.get("layers", []):
            for node in layer.get("ir_nodes", []):
                collect_identifiers(node)

        declarations = [{
            "type": "VariableDeclaration",
            "kind": "let",
            "name": name
        } for name in sorted(used)]

        # 将声明插入到第一个 layer 之前作为一个特殊 Layer
        if declarations:
            prog_dict["layers"].insert(0, {
                "name": "AutoDeclaredVariables",
                "layer_type": "internal",
                "ir_nodes": declarations,
                "children": []
            })

    @staticmethod
    def _convert_layer(layer):
        lines = []
        for node in layer["ir_nodes"]:
            lines.append(IRToJSLifter._convert_node(node))

        for child in layer.get("children", []):
            lines.extend(IRToJSLifter._convert_layer(child))
        return lines

    @staticmethod
    def _convert_node(node):
        t = node.get("type")

        if t == "VariableDeclaration":
            return f"{node['kind']} {node['name']};"

        if t == "AssignmentExpression":
            return f"{node['target']} = {IRToJSLifter._convert_node(node['value'])};"

        if t == "MemberExpression":
            return f"{node['object']}.{node['property']}"

        if t == "FunctionExpression":
            body = "\n  ".join(IRToJSLifter._convert_node(stmt) for stmt in node["body"])
            return f"(event) => {{\n  {body}\n}}"

        if t == "CallExpression":
            args = ", ".join(IRToJSLifter._convert_node(arg) for arg in node["args"])
            call = f"{IRToJSLifter._convert_node(node['callee_object'])}.{node['callee_method']}({args})"
            return f"const {node['result_name']} = {call};" if node.get("result_name") else call + ";"

        if t == "Identifier":
            return node["name"]

        if t == "Literal":
            val = node["value"]
            return json.dumps(val)

        raise ValueError(f"Unknown node type: {t}")
