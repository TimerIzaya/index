from typing import List, Union, Optional

from IR.IRType import Type
from config import OPTIONAL_JUMP


class IRNode:
    def to_dict(self):
        raise NotImplementedError


class Identifier(IRNode):
    def __init__(self, raw: str):
        self.raw = raw

    def to_dict(self):
        return {
            "type": "Identifier",
            "raw": self.raw
        }


'''
显示声明变量，例如var x = "123"，那么一个variable一定和一个identifier
隐式声明变量，例如funcx(KeyRanger.bound(1))，variable就不需要identifier
但是隐式声明是对资源的一种浪漫，我们希望声明的变量可以在上下文随意调用，所以这里我选择把identifier和variable绑定
我们IR中变量的name，其实就是它的identifier
'''
class Variable(IRNode):
    def to_dict(self):
        return {
            "type": "Variable",
            "name": self.name.to_dict(),
            "type": self.type.typename
        }

    def __init__(self, name: str, type_: Type):
        self.name = Identifier(name)
        self.type = type_

    def __repr__(self):
        return f"<Variable {self.name}: {self.type.typename}>"


class Literal(IRNode):
    def __init__(self, value: Union[str, int, float, bool, dict, None]):
        self.value = value

    def to_dict(self):
        return {
            "type": "Literal",
            "value": self.value
        }


'''
1. KeyRange.bound()
2. var x = ClassA; x.fieldA;
静态方法调用和成员变量调用都是member expression，目前我们仅支持以上两种，实际还有更多，但是测试idb不需要，如果有再继续兼容即可
'''
class MemberExpression(IRNode):
    def __init__(self, objectExpr: IRNode, property_name: str):
        assert isinstance(objectExpr, Identifier) or isinstance(objectExpr, Variable) or isinstance(objectExpr, self.__class__)
        # callee_object统一作为identifier处理
        if isinstance(objectExpr, Variable):
            objectExpr = objectExpr.name
        self.objectExpr = objectExpr
        self.property_name = property_name

    def to_dict(self):
        return {
            "type": "MemberExpression",
            "object": self.objectExpr.to_dict(),
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
    def __init__(self, callee_object: Union[Identifier, Variable], callee_method: str,
                 args: List[IRNode], result_name: Optional[str] = None):
        assert isinstance(callee_object, Identifier) or isinstance(callee_object, Variable)
        # callee_object统一作为identifier处理
        if isinstance(callee_object, Variable):
            callee_object = callee_object.name
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
            return Identifier(d["raw"])
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
                objectExpr=IRNodeFactory.from_dict(d["object"]),
                property_name=d["property"]
            )
        elif t == "FunctionExpression":
            return FunctionExpression(
                params=[Identifier(p["raw"]) for p in d.get("params", [])],
                body=[IRNodeFactory.from_dict(b) for b in d.get("body", [])]
            )

        elif t == "CallExpression":
            return CallExpression(
                callee_object=Identifier(d["callee_object"]["raw"]),
                callee_method=d["callee_method"],
                args=[IRNodeFactory.from_dict(arg) for arg in d.get("args", [])],
                result_name=d.get("result_name")
            )
        elif t == "ConsoleLog":
            return ConsoleLog(IRNodeFactory.from_dict(d["value"]))
        else:
            raise ValueError(f"Unknown IR node type: {t}")
