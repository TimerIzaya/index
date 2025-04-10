from enum import Enum

from IR.IRNodes import *
from IR.IRNodes import IRNode


# === 枚举 Layer 的 4 种类型 ===
class LayerType(Enum):
    CALLING = "调用型"
    REGISTER = "注册型"
    EXECUTION = "执行型"
    ACCESS = "访问型"

class Layer:
    def __init__(self, name: str, ir_nodes=None, children=None, layer_type: LayerType = LayerType.EXECUTION):
        self.name = name
        self.ir_nodes = ir_nodes or []
        self.children = children or []
        self.layer_type = layer_type

    def to_dict(self):
        return {
            "type": "Layer",
            "name": self.name,
            "layer_type": self.layer_type.value,
            "ir_nodes": [node.to_dict() for node in self.ir_nodes],
            "children": [child.to_dict() for child in self.children]
        }

    @staticmethod
    def from_dict(d: dict) -> 'Layer':
        return Layer(
            name=d["name"],
            layer_type=d.get("layer_type"),
            ir_nodes=[IRNodeFactory.from_dict(n) for n in d.get("ir_nodes", [])],
            children=[Layer.from_dict(c) for c in d.get("children", [])],
        )


class IRNodeFactory:
    @staticmethod
    def from_dict(d: dict) -> IRNode:
        t = d.get("type")
        if t == "Identifier":
            return Identifier(d["name"])
        elif t == "Literal":
            return Literal(d["value"])
        elif t == "VariableDeclaration":
            return VariableDeclaration(
                name=d["name"],
                kind=d.get("kind", "let")
            )
        elif t == "AssignmentExpression":
            return AssignmentExpression(
                left=IRNodeFactory.from_dict(d["left"]),
                right=IRNodeFactory.from_dict(d["right"])
            )
        elif t == "MemberExpression":
            return MemberExpression(
                object_expr=IRNodeFactory.from_dict(d["object"]),
                property_name=d["property"]
            )
        elif t == "FunctionExpression":
            return FunctionExpression(
                params=[IRNodeFactory.from_dict(p) for p in d.get("params", [])],
                body=[IRNodeFactory.from_dict(b) for b in d.get("body", [])]
            )
        elif t == "CallExpression":
            return CallExpression(
                callee_object=IRNodeFactory.from_dict(d["callee_object"]),
                callee_method=d["callee_method"],
                args=[IRNodeFactory.from_dict(arg) for arg in d.get("args", [])],
                result_name=d.get("result_name")
            )
        else:
            raise ValueError(f"Unknown IR node type: {t}")

