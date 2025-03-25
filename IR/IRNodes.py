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


class Program(IRNode):
    def __init__(self, layers):
        self.layers = layers

    def to_dict(self):
        return {
            "type": "Program",
            "layers": [layer.to_dict() for layer in self.layers]
        }
