from typing import List, Union, Optional

from config import OPTIONAL_JUMP


class IRNode:
    def to_dict(self):
        raise NotImplementedError


class Literal(IRNode):
    def __init__(self, value: Union[str, int, float, bool, dict, None]):
        self.value = value

    def to_dict(self):
        return {
            "type": "Literal",
            "value": self.value
        }


class Identifier(IRNode):
    def __init__(self, name: str):
        self.name = name

    def to_dict(self):
        return {
            "type": "Identifier",
            "name": self.name
        }


class MemberExpression(IRNode):
    def __init__(self, object_expr: IRNode, property_name: str):
        assert isinstance(object_expr, IRNode), "object_expr must be IRNode"
        self.object_expr = object_expr
        self.property_name = property_name

    def to_dict(self):
        return {
            "type": "MemberExpression",
            "object": self.object_expr.to_dict(),
            "property": self.property_name
        }


class AssignmentExpression(IRNode):
    def __init__(self, left: IRNode, right: IRNode):
        assert isinstance(left, IRNode), "left must be IRNode"
        assert isinstance(right, IRNode), "right must be IRNode"
        self.left = left
        self.right = right

    def to_dict(self):
        return {
            "type": "AssignmentExpression",
            "left": self.left.to_dict(),
            "right": self.right.to_dict()
        }



class CallExpression(IRNode):
    def __init__(self, callee_object: Identifier, callee_method: str,
                 args: List[IRNode], result_name: Optional[str] = None):
        assert isinstance(callee_object, Identifier)

        # 过滤掉 Literal("__JUMP__")
        filtered_args = []
        for arg in args:
            if isinstance(arg, Literal) and arg.value == OPTIONAL_JUMP:
                continue
            assert isinstance(arg, IRNode), f"Invalid arg: {arg}"
            filtered_args.append(arg)

        self.callee_object = callee_object
        self.callee_method = callee_method
        self.args = filtered_args
        self.result_name = result_name

    def to_dict(self):
        return {
            "type": "CallExpression",
            "callee_object": self.callee_object.to_dict(),
            "callee_method": self.callee_method,
            "args": [arg.to_dict() for arg in self.args],
            "result_name": self.result_name
        }

class FunctionExpression(IRNode):
    def __init__(self, params: List[Identifier], body: List[IRNode]):
        assert all(isinstance(p, Identifier) for p in params), "All params must be Identifier"
        self.params = params
        self.body = body

    def to_dict(self):
        return {
            "type": "FunctionExpression",
            "params": [p.to_dict() for p in self.params],
            "body": [stmt.to_dict() for stmt in self.body]
        }


class VariableDeclaration(IRNode):
    def __init__(self, name: str, kind: str = ""):
        self.name = name
        self.kind = kind  # let, const, var

    def to_dict(self):
        return {
            "type": "VariableDeclaration",
            "kind": self.kind,
            "name": self.name
        }


class ConsoleLog(IRNode):
    def __init__(self, value: IRNode):
        assert isinstance(value, IRNode), "value must be an IRNode"
        self.value = value

    def to_dict(self):
        return {
            "type": "ConsoleLog",
            "value": self.value.to_dict()
        }

    @staticmethod
    def from_dict(d: dict):
        return ConsoleLog(IRNodeFactory.from_dict(d["value"]))


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
                params=[Identifier(p["name"]) for p in d.get("params", [])],
                body=[IRNodeFactory.from_dict(b) for b in d.get("body", [])]
            )

        elif t == "CallExpression":
            return CallExpression(
                callee_object=Identifier(d["callee_object"]["name"]),
                callee_method=d["callee_method"],
                args=[IRNodeFactory.from_dict(arg) for arg in d.get("args", [])],
                result_name=d.get("result_name")
            )
        elif t == "ConsoleLog":
            return ConsoleLog(IRNodeFactory.from_dict(d["value"]))
        else:
            raise ValueError(f"Unknown IR node type: {t}")