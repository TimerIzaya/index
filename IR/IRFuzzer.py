import random
from .IRNodes import *
from .IRParamGenerator import ParameterGenerator
from .IRSchemaParser import IndexedDBSchemaParser


class IRFuzzer:
    def __init__(self, schema_path, max_nodes=50, config=None):
        self.schema_parser = IndexedDBSchemaParser(schema_path)
        self.param_gen = ParameterGenerator()
        self.max_nodes = max_nodes
        self.config = config or {
            "enable_onupgradeneeded": True,
            "enable_onsuccess": True,
            "enable_transaction": True,
            "enable_store_ops": True,
            "num_transactions": (1, 3),
            "ops_per_transaction": (1, 3)
        }
        self.var_counter = 0

    def _new_var(self, prefix="tmp"):
        self.var_counter += 1
        return f"{prefix}{self.var_counter}"

    def generate_program(self) -> Program:
        program = Program()
        self._generate_open_call(program)
        return program

    def _generate_open_call(self, program: Program):
        db_name = Literal("fuzzDB")
        db_version = Literal(random.randint(1, 10))
        open_var = self._new_var("req")

        call = CallExpression(
            object_name="indexedDB",
            property_name="open",
            arguments=[db_name, db_version],
            result_name=open_var,
            handlers={}
        )

        if self.config.get("enable_onupgradeneeded", True):
            up_fn = FunctionBody(params=["event"])
            self._generate_onupgradeneeded("event", up_fn)
            call.add_handler("onupgradeneeded", up_fn)

        if self.config.get("enable_onsuccess", True):
            success_fn = FunctionBody(params=["event"])
            self._generate_onsuccess("event", success_fn)
            call.add_handler("onsuccess", success_fn)

        program.add(call)

    def _generate_onupgradeneeded(self, event_var: str, body: FunctionBody):
        db_var = self._new_var("db")
        db_access = MemberExpression(object_name=event_var + ".target", property_name="result")
        db_decl = VariableDeclaration(name=db_var, value=db_access)
        body.add(db_decl)

        store_name = Literal("store1")
        create_call = CallExpression(
            object_name=db_var,
            property_name="createObjectStore",
            arguments=[store_name]
        )
        body.add(create_call)

    def _generate_onsuccess(self, event_var: str, body: FunctionBody):
        db_var = self._new_var("db")
        db_access = MemberExpression(object_name=event_var + ".target", property_name="result")
        db_decl = VariableDeclaration(name=db_var, value=db_access)
        body.add(db_decl)

        if self.config.get("enable_transaction", True):
            self._generate_transactions(db_var, body)

    def _generate_transactions(self, db_var: str, body: FunctionBody):
        num_txns = random.randint(*self.config.get("num_transactions", (1, 1)))
        for _ in range(num_txns):
            txn_var = self._new_var("txn")
            store_list = Literal("store1")
            txn_call = CallExpression(
                object_name=db_var,
                property_name="transaction",
                arguments=[store_list],
                result_name=txn_var
            )
            body.add(txn_call)

            if self.config.get("enable_store_ops", True):
                self._generate_store_ops(txn_var, body)

    def _generate_store_ops(self, txn_var: str, body: FunctionBody):
        store_var = self._new_var("store")
        get_store = CallExpression(
            object_name=txn_var,
            property_name="objectStore",
            arguments=[Literal("store1")],
            result_name=store_var
        )
        body.add(get_store)

        num_ops = random.randint(*self.config.get("ops_per_transaction", (1, 1)))
        ops = ["get", "add", "put", "delete"]
        for _ in range(num_ops):
            method = random.choice(ops)
            params = [Literal("key" if method == "get" else "value")]
            if method in ("add", "put") and random.random() < 0.5:
                params.append(Literal("optionalKey"))

            op_call = CallExpression(
                object_name=store_var,
                property_name=method,
                arguments=params
            )
            body.add(op_call)
