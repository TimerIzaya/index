from typing import List, Dict, Optional, Any, Union


class IRNode:
    is_expression: bool = False
    is_statement: bool = False
    has_scope: bool = False

    def to_dict(self) -> dict:
        raise NotImplementedError()

    def __repr__(self):
        return str(self.to_dict())

class Literal(IRNode):
    is_expression = True

    def __init__(self, value: Any):
        self.value = value

    def to_dict(self):
        return {
            "type": "Literal",
            "value": self.value
        }

class MemberExpression(IRNode):
    is_expression = True

    def __init__(self, object_name: str, property_name: str):
        self.object_name = object_name
        self.property_name = property_name

    def to_dict(self):
        return {
            "type": "MemberExpression",
            "object": self.object_name,
            "property": self.property_name
        }

class VariableDeclaration(IRNode):
    is_statement = True

    def __init__(self, name: str, value: IRNode):
        self.name = name
        self.value = value

    def to_dict(self):
        return {
            "type": "VariableDeclaration",
            "name": self.name,
            "value": self.value.to_dict()
        }

class CallExpression(IRNode):
    is_expression = True
    is_statement = True

    def __init__(
        self,
        object_name: str,
        property_name: str,
        arguments: List[IRNode],
        result_name: Optional[str] = None,
        handlers: Optional[Dict[str, 'FunctionBody']] = None
    ):
        self.object_name = object_name
        self.property_name = property_name
        self.arguments = arguments
        self.result_name = result_name
        self.handlers = handlers or {}

    def add_handler(self, event: str, handler: 'FunctionBody'):
        self.handlers[event] = handler

    def to_dict(self):
        return {
            "type": "CallExpression",
            "callee": {
                "object": self.object_name,
                "property": self.property_name
            },
            "arguments": [arg.to_dict() for arg in self.arguments],
            "resultName": self.result_name,
            "handlers": {
                key: handler.to_dict()
                for key, handler in self.handlers.items()
            } if self.handlers else None
        }

class FunctionBody(IRNode):
    has_scope = True

    def __init__(self, params: List[str], body: Optional[List[IRNode]] = None):
        self.params = params
        self.body = body or []

    def add(self, node: IRNode):
        self.body.append(node)

    def to_dict(self):
        return {
            "type": "FunctionBody",
            "params": self.params,
            "body": [node.to_dict() for node in self.body]
        }

class TryCatchBlock(IRNode):
    is_statement = True
    has_scope = True

    def __init__(self, try_body: List[IRNode], catch_param: str, catch_body: List[IRNode]):
        self.try_body = try_body
        self.catch_param = catch_param
        self.catch_body = catch_body

    def to_dict(self):
        return {
            "type": "TryCatchBlock",
            "try": [stmt.to_dict() for stmt in self.try_body],
            "catch": {
                "param": self.catch_param,
                "body": [stmt.to_dict() for stmt in self.catch_body]
            }
        }

class IfStatement(IRNode):
    is_statement = True
    has_scope = True

    def __init__(self, test: IRNode, consequent: List[IRNode], alternate: Optional[List[IRNode]] = None):
        self.test = test
        self.consequent = consequent
        self.alternate = alternate or []

    def to_dict(self):
        return {
            "type": "IfStatement",
            "test": self.test.to_dict(),
            "consequent": [stmt.to_dict() for stmt in self.consequent],
            "alternate": [stmt.to_dict() for stmt in self.alternate] if self.alternate else None
        }

class Program(IRNode):
    is_statement = True
    has_scope = True

    def __init__(self):
        self.body: List[IRNode] = []

    def add(self, node: IRNode):
        self.body.append(node)

    def to_dict(self):
        return {
            "type": "Program",
            "body": [node.to_dict() for node in self.body]
        }