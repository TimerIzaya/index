class IRNode:
    def to_dict(self):
        raise NotImplementedError()


class Literal(IRNode):
    def __init__(self, value, type=None):
        self.value = value
        self.type = type  # optional, e.g., "string", "number"

    def to_dict(self):
        return {
            "type": "Literal",
            "value": self.value,
            "valueType": self.type
        }


class Identifier(IRNode):
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            "type": "Identifier",
            "name": self.name
        }


class CallExpression(IRNode):
    def __init__(self, callee_object, callee_method, args, result_name=None):
        self.callee_object = callee_object
        self.callee_method = callee_method
        self.args = args  # List of IRNode (e.g., Literal, Identifier)
        self.result_name = result_name  # optional name to store result

    def to_dict(self):
        return {
            "type": "CallExpression",
            "callee_object": self.callee_object,
            "callee_method": self.callee_method,
            "args": [arg.to_dict() for arg in self.args],
            "result_name": self.result_name
        }


class AssignmentExpression(IRNode):
    def __init__(self, target, value):
        self.target = target  # string
        self.value = value    # IRNode, typically FunctionExpression

    def to_dict(self):
        return {
            "type": "AssignmentExpression",
            "target": self.target,
            "value": self.value.to_dict()
        }


class FunctionExpression(IRNode):
    def __init__(self, params, body):
        self.params = params  # list of strings
        self.body = body      # list of IRNode (e.g., CallExpression, Assignment)

    def to_dict(self):
        return {
            "type": "FunctionExpression",
            "params": self.params,
            "body": [stmt.to_dict() for stmt in self.body]
        }


class ReturnStatement(IRNode):
    def __init__(self, value: IRNode):
        self.value = value

    def to_dict(self):
        return {
            "type": "ReturnStatement",
            "value": self.value.to_dict()
        }