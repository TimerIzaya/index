from IR.CallExpression import CallExpression
from IR.IRNode import IRNode
from typing import List, Dict, Optional, Any, Union


class Program(IRNode):
    def __init__(self):
        self.body: List[IRNode] = []

    def add(self, node: IRNode):
        self.body.append(node)

    def to_dict(self):
        return {
            "type": "Program",
            "body": [node.to_dict() for node in self.body]
        }




if __name__ == '__main__':
    program = Program()
    program.add(CallExpression("indexedDB", "open", ["mydb"]))
    print(program.to_dict())
