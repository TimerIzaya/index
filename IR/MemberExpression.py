from IR.IRNode import IRNode


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


if __name__ == '__main__':
    expr = MemberExpression("event.target", "result")
    print(expr.to_dict())
