import random
import json

from IR.IRSchemaParser import IndexedDBSchemaParser
from IR.ParamGenerator import ParameterGenerator
from IRNodes import *

class IRContext:
    def __init__(self):
        self.scope_stack = [{}]

    def push_scope(self):
        self.scope_stack.append({})

    def pop_scope(self):
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()

    def register(self, name, type_):
        self.scope_stack[-1][name] = type_

    def is_defined(self, name):
        return any(name in scope for scope in reversed(self.scope_stack))

    def get_var_by_type(self, type_):
        for scope in reversed(self.scope_stack):
            for name, t in scope.items():
                if t == type_:
                    return name
        return None

class IRFuzzer:
    def __init__(self):
        self.schema = IndexedDBSchemaParser()
        self.param_gen = ParameterGenerator()
        self.context = IRContext()

    def generate_program(self):
        program = Program()
        open_stmt = self.generate_open_call()
        if open_stmt:
            program.add(open_stmt)
        return program

    def generate_open_call(self):
        method = self.schema.get_static_methods("IDBFactory").get("open")
        if not method:
            return None

        params = method.get("parameters", [])
        args = self.param_gen.generate_arguments(params)
        open_call = CallExpression("indexedDB", "open", [Literal(arg) for arg in args], result_name="request")
        self.context.register("request", "IDBOpenDBRequest")

        self.context.push_scope()
        handler_body = []

        db_decl = VariableDeclaration("db", MemberExpression("event.target", "result"))
        self.context.register("db", "IDBDatabase")
        handler_body.append(db_decl)

        tx_method = self.schema.get_instance_methods("IDBDatabase").get("transaction")
        if tx_method:
            tx_params = self.schema.get_parameters("IDBDatabase", "transaction")
            tx_args = self.param_gen.generate_arguments(tx_params)
            tx_call = CallExpression("db", "transaction", [Literal(arg) for arg in tx_args], result_name="tx")
            self.context.register("tx", "IDBTransaction")
            handler_body.append(tx_call)

            store_call = CallExpression("tx", "objectStore", [Literal("store1")], result_name="store")
            self.context.register("store", "IDBObjectStore")
            handler_body.append(store_call)

            put_method = self.schema.get_instance_methods("IDBObjectStore").get("put")
            if put_method:
                put_params = self.schema.get_parameters("IDBObjectStore", "put")
                put_args = self.param_gen.generate_arguments(put_params)
                put_call = CallExpression("store", "put", [Literal(arg) for arg in put_args])
                handler_body.append(put_call)

        self.context.pop_scope()

        onsuccess_fn = FunctionBody(["event"], handler_body)
        open_call.add_handler("onsuccess", onsuccess_fn)
        return open_call

if __name__ == "__main__":
    fuzzer = IRFuzzer()
    program = fuzzer.generate_program()

    def patched_call_to_dict(self):
        data = {
            "type": "CallExpression",
            "object": self.object_name,
            "property": self.property_name,
            "arguments": [arg.to_dict() if hasattr(arg, "to_dict") else arg for arg in self.arguments]
        }
        if self.result_name:
            data["result"] = self.result_name
        if self.handlers:
            data["handlers"] = {k: v.to_dict() for k, v in self.handlers.items()}
        return data

    CallExpression.to_dict = patched_call_to_dict

    print(json.dumps(program.to_dict(), indent=2))
