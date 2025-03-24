from typing import List, Optional, Union


class IRNode:
    def to_dict(self) -> dict:
        raise NotImplementedError()


# ========= Identifier =========
class Identifier(IRNode):
    def __init__(self, name: str):
        self.name: str = name

    def to_dict(self) -> dict:
        return {
            "type": "Identifier",
            "name": self.name
        }


# ========= Literal =========
class Literal(IRNode):
    def __init__(self, value: Union[str, int, float, bool, None], type: Optional[str] = None):
        self.value = value
        self.value_type = type or self._infer_type()

    def _infer_type(self) -> str:
        if isinstance(self.value, str):
            return "string"
        elif isinstance(self.value, bool):
            return "boolean"
        elif isinstance(self.value, (int, float)):
            return "number"
        elif self.value is None:
            return "null"
        else:
            return "any"

    def to_dict(self) -> dict:
        return {
            "type": "Literal",
            "value": self.value,
            "valueType": self.value_type
        }


# ========= CallExpression =========
class CallExpression(IRNode):
    def __init__(
        self,
        callee_object: Identifier,
        callee_method: str,
        args: List[IRNode],
        result_name: Optional[str] = None
    ):
        self.callee_object = callee_object
        self.callee_method = callee_method
        self.args = args
        self.result_name = result_name

    def to_dict(self) -> dict:
        return {
            "type": "CallExpression",
            "callee_object": self.callee_object.to_dict(),
            "callee_method": self.callee_method,
            "args": [arg.to_dict() for arg in self.args],
            "result_name": self.result_name
        }


# ========= AssignmentExpression =========
class AssignmentExpression(IRNode):
    def __init__(self, left: str, right: IRNode):
        self.left = left  # e.g. "db.onversionchange"
        self.right = right

    def to_dict(self) -> dict:
        return {
            "type": "AssignmentExpression",
            "left": self.left,
            "right": self.right.to_dict()
        }

# ========= FunctionExpression =========
class FunctionExpression(IRNode):
    def __init__(self, params: List[str], body: List[IRNode]):
        self.params = params
        self.body = body

    def to_dict(self) -> dict:
        return {
            "type": "FunctionExpression",
            "params": self.params,
            "body": [stmt.to_dict() for stmt in self.body]
        }


# ========= Program =========
class Program(IRNode):
    def __init__(self, body: List[IRNode]):
        self.body = body

    def to_dict(self) -> dict:
        return {
            "type": "Program",
            "body": [stmt.to_dict() for stmt in self.body]
        }
