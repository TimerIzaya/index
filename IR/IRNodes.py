from typing import List


class IRNode:
    def to_dict(self):
        raise NotImplementedError()


class Identifier(IRNode):
    def __init__(self, name: str):
        self.name = name

    def to_dict(self):
        return {
            "type": "Identifier",
            "name": self.name
        }


class Literal(IRNode):
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {
            "type": "Literal",
            "value": self.value
        }


class MemberExpression(IRNode):
    def __init__(self, object_name: str, property_name: str):
        self.object_name = object_name
        self.property_name = property_name

    def to_dict(self):
        return {
            "type": "MemberExpression",
            "object": self.object_name,
            "property": self.property_name
        }


class AssignmentExpression(IRNode):
    def __init__(self, target: str, value: IRNode):
        self.target = target
        self.value = value

    def to_dict(self):
        return {
            "type": "AssignmentExpression",
            "target": self.target,
            "value": self.value.to_dict()
        }


class FunctionExpression(IRNode):
    def __init__(self, params, body):
        self.params = params  # List[str]
        self.body = body  # List[IRNode]

    def to_dict(self):
        return {
            "type": "FunctionExpression",
            "params": self.params,
            "body": [stmt.to_dict() for stmt in self.body]
        }


class CallExpression(IRNode):
    def __init__(self, callee_object: IRNode, callee_method: str, args, result_name=None):
        self.callee_object = callee_object  # IRNode (typically Identifier)
        self.callee_method = callee_method
        self.args = args  # List[IRNode or raw value]
        self.result_name = result_name

    def to_dict(self):
        def wrap(arg):
            return arg.to_dict() if isinstance(arg, IRNode) else Literal(arg).to_dict()

        return {
            "type": "CallExpression",
            "callee_object": self.callee_object.to_dict(),
            "callee_method": self.callee_method,
            "args": [wrap(arg) for arg in self.args],
            "result_name": self.result_name
        }


class Program:
    def __init__(self, layers: List["Layer"]):
        self.layers = layers

    def to_dict(self):
        return {
            "type": "Program",
            "layers": [layer.to_dict() for layer in self.layers]
        }

    @staticmethod
    def from_dict(d: dict):
        from layers.Layer import Layer
        return Program([Layer.from_dict(ld) for ld in d.get("layers", [])])

class VariableDeclaration(IRNode):
    def __init__(self, kind: str, name: str):
        self.kind = kind  # typically 'let'
        self.name = name

    def to_dict(self):
        return {
            "type": "VariableDeclaration",
            "kind": self.kind,
            "name": self.name
        }


class IRNodeFactory:
    @staticmethod
    def from_dict(d: dict):
        t = d.get("type")
        if t == "CallExpression":
            return CallExpression(
                callee_object=IRNodeFactory.from_dict(d["callee_object"]),
                callee_method=d["callee_method"],
                args=[IRNodeFactory.from_dict(arg) for arg in d["args"]],
                result_name=d.get("result_name")
            )
        elif t == "AssignmentExpression":
            return AssignmentExpression(
                target=d["target"],
                value=IRNodeFactory.from_dict(d["value"])
            )
        elif t == "FunctionExpression":
            return FunctionExpression(
                params=d.get("params", []),
                body=[IRNodeFactory.from_dict(n) for n in d["body"]]
            )
        elif t == "MemberExpression":
            return MemberExpression(d["object"], d["property"])
        elif t == "Identifier":
            return Identifier(d["name"])
        elif t == "Literal":
            return Literal(d["value"])
        elif t == "VariableDeclaration":
            return VariableDeclaration(d["kind"], d["name"])
        else:
            raise ValueError(f"Unknown node type: {t}")
