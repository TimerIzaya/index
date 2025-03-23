class Layer:
    def __init__(self, name, ir_nodes=None, children=None):
        self.name = name
        self.ir_nodes = ir_nodes or []
        self.children = children or []

    def to_dict(self):
        return {
            "type": "Layer",
            "name": self.name,
            "ir_nodes": [node.to_dict() for node in self.ir_nodes],
            "children": [child.to_dict() for child in self.children]
        }


class Program:
    def __init__(self, layers=None):
        self.layers = layers or []

    def to_dict(self):
        return {
            "type": "Program",
            "layers": [layer.to_dict() for layer in self.layers]
        }