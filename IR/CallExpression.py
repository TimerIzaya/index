from typing import List, Dict, Optional, Any, Union
from IR.IRNode import IRNode

class CallExpression(IRNode):
    def __init__(
        self,
        object_name: str,
        property_name: str,
        arguments: List[Any],
        result_name: Optional[str] = None,
        handlers: Optional[Dict[str, 'FunctionBody.py']] = None
    ):
        self.object_name = object_name
        self.property_name = property_name
        self.arguments = arguments
        self.result_name = result_name
        self.handlers = handlers or {}

    def add_handler(self, event: str, handler: 'FunctionBody.py'):
        self.handlers[event] = handler

    def to_dict(self):
        return {
            "type": "CallExpression",
            "callee": {
                "object": self.object_name,
                "property": self.property_name
            },
            "arguments": self.arguments,
            "resultName": self.result_name,
            "handlers": {
                key: handler.to_dict()
                for key, handler in self.handlers.items()
            } if self.handlers else None
        }
