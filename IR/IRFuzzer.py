import random
import json
from IRNodes import *
from IR.IRSchemaParser import IndexedDBSchemaParser
from IR.ParamGenerator import ParameterGenerator


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
    def __init__(self, max_nodes=100):
        self.schema = IndexedDBSchemaParser()
        self.param_gen = ParameterGenerator()
        self.context = IRContext()
        self.max_nodes = max_nodes
        self.node_count = 0

    def _add_node(self, node, body):
        if self.node_count >= self.max_nodes:
            return False
        body.append(node)
        self.node_count += 1
        return True

    def generate_program(self):
        program = Program()
        open_stmt = self.generate_open_db()
        if open_stmt:
            program.add(open_stmt)
        return program

    def generate_open_db(self):
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
        self._add_node(db_decl, handler_body)

        tx_stmt = self.generate_transaction_block()
        if tx_stmt:
            for stmt in tx_stmt:
                if not self._add_node(stmt, handler_body):
                    break

        self.context.pop_scope()

        onsuccess_fn = FunctionBody(["event"], handler_body)
        open_call.add_handler("onsuccess", onsuccess_fn)
        return open_call

    def generate_transaction_block(self):
        method = self.schema.get_instance_methods("IDBDatabase").get("transaction")
        if not method:
            return []

        tx_params = method.get("parameters", [])
        tx_args = self.param_gen.generate_arguments(tx_params)
        tx_call = CallExpression("db", "transaction", [Literal(arg) for arg in tx_args], result_name="tx")
        self.context.register("tx", "IDBTransaction")

        store_call = CallExpression("tx", "objectStore", [Literal("store1")], result_name="store")
        self.context.register("store", "IDBObjectStore")

        store_block = self.generate_object_store_operations()

        return [tx_call, store_call] + store_block

    def generate_object_store_operations(self):

        body = []
        for method_name, method_info in self.schema.get_instance_methods("IDBObjectStore").items():
            if self.node_count >= self.max_nodes:
                break
            if random.random() < 0.5:
                params = method_info.get("parameters", [])
                args = self.param_gen.generate_arguments(params)
                call = CallExpression("store", method_name, [Literal(arg) for arg in args],
                                      result_name=f"{method_name}Result")
                self.context.register(f"{method_name}Result", method_info.get("returns", "unknown"))

                for evt in self.schema.get_events(method_info.get("returns", "").strip()):
                    if evt["name"].startswith("on"):
                        handler = FunctionBody(["event"], [
                            VariableDeclaration("result", MemberExpression("event.target", "result"))
                        ])
                        call.add_handler(evt["name"], handler)

                if not self._add_node(call, body):
                    break

        for prop_name, prop_info in self.schema.get_properties("IDBObjectStore").items():
            if self.node_count >= self.max_nodes:
                break
            get_before = MemberExpression("store", prop_name)
            if not self._add_node(VariableDeclaration(f"{prop_name}Value_before", get_before), body):
                break

            if not prop_info.get("readonly", False):
                new_value = self.param_gen._generate_by_type(prop_info.get("type", "string"))
                assign = Assignment(MemberExpression("store", prop_name), Literal(new_value))
                if not self._add_node(assign, body):
                    break

                get_after = MemberExpression("store", prop_name)
                if not self._add_node(VariableDeclaration(f"{prop_name}Value_after", get_after), body):
                    break

                if random.random() < 0.3:
                    condition = BinaryExpression("!=", f"{prop_name}Value_after", f"{prop_name}Value_before")
                    then_block = [CallExpression("console", "log", [Literal(f"{prop_name} value mismatch!")])]
                    self._add_node(IfStatement(condition, then_block), body)
        return body  # limited to self.remaining_ops total operations


if __name__ == "__main__":
    import shutil
    from datetime import datetime
    import os

    output_dir = os.path.join("IR", "generated")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    for i in range(10):  # 生成10个IR
        fuzzer = IRFuzzer(max_nodes=300)
        program = fuzzer.generate_program()

        filename = f"ir_{i + 1:03d}.json"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w") as f:
            json.dump(program.to_dict(), f, indent=2)

        print(f"IR saved to {filepath}")
