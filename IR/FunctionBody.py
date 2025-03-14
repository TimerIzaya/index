from IR.IRNode import IRNode
from typing import List, Dict, Optional, Any, Union

from IR.MemberExpression import MemberExpression
from IR.VariableDeclaration import VariableDeclaration


class FunctionBody(IRNode):
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


if __name__ == '__main__':
    func = FunctionBody(["event"])
    func.add(VariableDeclaration("db", MemberExpression("event.target", "result")))
    print(func.to_dict())
