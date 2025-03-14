from IR.IRNode import IRNode
from IR.MemberExpression import MemberExpression


class VariableDeclaration(IRNode):
    def __init__(self, name: str, value: 'MemberExpression'):
        self.name = name
        self.value = value

    def to_dict(self):
        return {
            "type": "VariableDeclaration",
            "name": self.name,
            "value": self.value.to_dict()
        }


if __name__ == '__main__':
    var = VariableDeclaration("db", MemberExpression("event.target", "result"))
    print(var.to_dict())
