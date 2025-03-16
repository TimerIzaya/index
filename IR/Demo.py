import json
import random

# ------- 简化 IRNodes -------
class Literal:
    def __init__(self, value): self.value = value
    def to_dict(self): return {"type": "Literal", "value": self.value}

class MemberExpression:
    def __init__(self, obj, prop): self.obj = obj; self.prop = prop
    def to_dict(self): return {"type": "MemberExpression", "object": self.obj, "property": self.prop}

class VariableDeclaration:
    def __init__(self, name, value): self.name = name; self.value = value
    def to_dict(self): return {"type": "VariableDeclaration", "name": self.name, "value": self.value.to_dict()}

class CallExpression:
    def __init__(self, obj, prop, args, result_name=None): self.object_name = obj; self.property_name = prop; self.arguments = args; self.result_name = result_name; self.handlers = {}
    def add_handler(self, name, func): self.handlers[name] = func
    def to_dict(self):
        return {
            "type": "CallExpression",
            "object": self.object_name,
            "property": self.property_name,
            "arguments": [arg.to_dict() for arg in self.arguments],
            **({"result": self.result_name} if self.result_name else {}),
            **({"handlers": {k: v.to_dict() for k, v in self.handlers.items()}} if self.handlers else {})
        }

class FunctionBody:
    def __init__(self, params, body): self.params = params; self.body = body
    def to_dict(self): return {"type": "FunctionBody", "params": self.params, "body": [stmt.to_dict() for stmt in self.body]}

class Program:
    def __init__(self): self.body = []
    def add(self, stmt): self.body.append(stmt)
    def to_dict(self): return {"type": "Program", "body": [stmt.to_dict() for stmt in self.body]}

# ------- IRFuzzer 最小测试 -------
program = Program()

open_call = CallExpression("indexedDB", "open", [Literal("myDB"), Literal(1)], result_name="request")

handler_body = [
    VariableDeclaration("db", MemberExpression("event.target", "result")),
    CallExpression("db", "transaction", [Literal("store1"), Literal("readwrite")], result_name="tx"),
    CallExpression("tx", "objectStore", [Literal("store1")], result_name="store"),
    CallExpression("store", "put", [Literal({"name": "Alice"}), Literal(1)])
]

onsuccess_fn = FunctionBody(["event"], handler_body)
open_call.add_handler("onsuccess", onsuccess_fn)

program.add(open_call)

print(json.dumps(program.to_dict(), indent=2))
