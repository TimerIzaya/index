import sys
import unittest

sys.path.append('IR')

import config
from IR.IRFuzzer import *



class TestIRFuzzer(unittest.TestCase):

    def setUp(self):
        self.fuzzer = IRFuzzer(schema_path=config.SCHEMA_FILE, config={
            "enable_onupgradeneeded": True,
            "num_transactions": (1, 1),
            "ops_per_transaction": (1, 1)
        })

    def test_generate_program(self):
        program = self.fuzzer.generate_program()
        self.assertIsInstance(program, Program)
        self.assertGreater(len(program.body), 0)

    def test_open_call_layer(self):
        program = Program()
        self.fuzzer._generate_open_call(program)
        self.assertEqual(len(program.body), 1)
        call = program.body[0]
        self.assertIsInstance(call, CallExpression)
        self.assertEqual(call.property_name, "open")

    def test_onupgradeneeded_layer(self):
        body = FunctionBody(params=["event"])
        self.fuzzer._generate_onupgradeneeded("event", body)
        self.assertGreaterEqual(len(body.body), 2)
        self.assertIsInstance(body.body[0], VariableDeclaration)
        self.assertEqual(body.body[1].property_name, "createObjectStore")

    def test_onsuccess_layer(self):
        body = FunctionBody(params=["event"])
        self.fuzzer._generate_onsuccess("event", body)
        self.assertTrue(any(isinstance(node, CallExpression) and node.property_name == "transaction" for node in body.body))

    def test_transaction_layer(self):
        body = FunctionBody(params=[])
        self.fuzzer._generate_transactions("db1", body)
        found_txn = any(isinstance(n, CallExpression) and n.property_name == "transaction" for n in body.body)
        self.assertTrue(found_txn)

    def test_objectstore_ops_layer(self):
        body = FunctionBody(params=[])
        self.fuzzer._generate_store_ops("txn1", body)
        found_store = any(isinstance(n, CallExpression) and n.property_name == "objectStore" for n in body.body)
        self.assertTrue(found_store)
        found_op = any(isinstance(n, CallExpression) and n.property_name in ["get", "add", "put", "delete"] for n in body.body)
        self.assertTrue(found_op)

if __name__ == '__main__':
    unittest.main()
