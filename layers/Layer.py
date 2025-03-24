from enum import Enum

# === 枚举 Layer 的 4 种类型 ===
class LayerType(Enum):
    CALLING = "调用型"
    REGISTER = "注册型"
    EXECUTION = "执行型"
    ACCESS = "访问型"

# === Layer 基类 ===
class Layer:
    def __init__(self, name: str, ir_nodes=None, children=None, layer_type: LayerType = LayerType.EXECUTION):
        self.name = name
        self.ir_nodes = ir_nodes or []
        self.children = children or []
        self.layer_type = layer_type  # ✅ 新增类型字段

    def to_dict(self):
        return {
            "type": "Layer",
            "name": self.name,
            "layer_type": self.layer_type.value,
            "ir_nodes": [node.to_dict() for node in self.ir_nodes],
            "children": [child.to_dict() for child in self.children]
        }


# === IRProgram 顶层结构 ===
class Program:
    def __init__(self, layers=None):
        self.layers = layers or []

    def to_dict(self):
        return {
            "type": "Program",
            "layers": [layer.to_dict() for layer in self.layers]
        }
