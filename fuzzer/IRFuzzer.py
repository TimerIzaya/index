from random import random

from IR.IRNodes import *


class IRFuzzer:
    def __init__(self, schema):
        self.schema = schema
        self.context = IRContext()

    def generate_random_ir(self, depth=3):
        program = Program()
        for _ in range(depth):
            node = self.generate_random_operation()
            if node:
                program.add(node)
        return program

    def generate_random_operation(self):
        choices = [
            self.generate_open_db,
            self.generate_transaction,
            self.generate_object_store_op,
            self.generate_put,
            self.generate_try_catch
        ]
        return random.choice(choices)()

    def generate_open_db(self):
        db_name = f"db_{random.randint(1, 1000)}"
        open_call = CallExpression(
            object_name="indexedDB",
            property_name="open",
            arguments=[Literal(db_name), Literal(1)],
            result_name="request"
        )
        self.context.register_variable("request", "IDBOpenDBRequest")
        return open_call

    def generate_transaction(self):
        if not self.context.current_db:
            return None
        tx_name = f"tx_{random.randint(1, 1000)}"
        tx_call = CallExpression(
            object_name="db",
            property_name="transaction",
            arguments=[Literal(["store1"]), Literal("readwrite")],
            result_name=tx_name
        )
        self.context.register_variable(tx_name, "IDBTransaction")
        self.context.enter_transaction(tx_name)
        return tx_call

    def generate_object_store_op(self):
        if not self.context.has_active_transaction():
            return None
        store_name = f"store_{random.randint(1, 100)}"
        store_call = CallExpression(
            object_name="tx",
            property_name="objectStore",
            arguments=[Literal(store_name)],
            result_name="store"
        )
        self.context.register_variable("store", "IDBObjectStore")
        return store_call

    def generate_put(self):
        if not self.context.is_variable_defined("store"):
            return None
        data = {"name": "FuzzTest", "value": random.randint(1, 100)}
        put_call = CallExpression(
            object_name="store",
            property_name="put",
            arguments=[Literal(data), Literal(1)]
        )
        return put_call

    def generate_try_catch(self):
        try_body = [
            self.generate_transaction(),
            self.generate_object_store_op(),
            self.generate_put()
        ]
        catch_body = [
            CallExpression("console", "log", [Literal("Transaction failed")])
        ]
        return TryCatchBlock(
            try_body=[stmt for stmt in try_body if stmt is not None],
            catch_param="e",
            catch_body=catch_body
        )

if __name__ == "__main__":
    schema_parser = IndexedDBSchemaParser("indexeddb_schema.json")
    fuzzer = IRFuzzer(schema_parser)
    random_ir = fuzzer.generate_random_ir(depth=5)
    import json
    print(json.dumps(random_ir.to_dict(), indent=2))