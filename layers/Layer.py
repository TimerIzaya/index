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

    def to_dict(self) -> dict:
        result = {
            "name": self.name,
            "layer_type": self.layer_type.value,
        }

        if self.ir_nodes:
            result["ir_nodes"] = [n.to_dict() for n in self.ir_nodes]

        if self.children:
            children_serialized = [c.to_dict() for c in self.children if c is not None]
            if children_serialized:
                result["children"] = children_serialized

        return result

    @staticmethod
    def from_dict(d: dict) -> 'Layer':
        return Layer(
            name=d["name"],
            layer_type=LayerType(d.get("layer_type", LayerType.EXECUTION.value)),
            ir_nodes=[
                IRNodeFactory.from_dict(n) for n in d.get("ir_nodes", [])
                if n is not None
            ],
            children=[
                Layer.from_dict(c) for c in d.get("children", [])
                if c is not None
            ],
        )




