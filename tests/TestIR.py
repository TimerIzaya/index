import json
import unittest
import os

from IR.IRFuzzer import IRFuzzer


import config

SCHEMA_PATH = config.SCHEMA_FILE

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "ir_outputs")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
else:
    # 清空目录下所有文件
    for f in os.listdir(OUTPUT_DIR):
        file_path = os.path.join(OUTPUT_DIR, f)
        if os.path.isfile(file_path):
            os.remove(file_path)

class TestIRFuzzerLayers(unittest.TestCase):

    def _save_ir(self, name, program):
        path = os.path.join(OUTPUT_DIR, f"{name}.json")
        with open(path, "w") as f:
            json.dump(program.to_dict(), f, indent=2)
        print(f"Saved: {path}")

    # let req1 = indexedDB.open("fuzzDB", 10);
    def test_layer_1_only_open(self):
        fuzzer = IRFuzzer(SCHEMA_PATH, config={
            "enable_onupgradeneeded": False,
            "enable_onsuccess": False
        })
        program = fuzzer.generate_program()
        self._save_ir("layer1_open_only", program)

    # let req1 = indexedDB.open("fuzzDB", 10);
    # req1.onupgradeneeded = function(event)
    # {
    # let db2 = event.target.result;
    # db2.createObjectStore("store1");
    # };
    def test_layer_12_open_and_upgrade(self):
        fuzzer = IRFuzzer(SCHEMA_PATH, config={
            "enable_onupgradeneeded": True,
            "enable_onsuccess": False
        })
        program = fuzzer.generate_program()
        self._save_ir("layer12_open_and_upgrade", program)

    def test_layer_123_open_upgrade_success(self):
        fuzzer = IRFuzzer(SCHEMA_PATH, config={
            "enable_onupgradeneeded": True,
            "enable_onsuccess": True,
            "enable_transaction": False
        })
        program = fuzzer.generate_program()
        self._save_ir("layer123_open_upgrade_success", program)

    def test_layer_1234_include_transaction(self):
        fuzzer = IRFuzzer(SCHEMA_PATH, config={
            "enable_onupgradeneeded": True,
            "enable_onsuccess": True,
            "enable_transaction": True,
            "enable_store_ops": False
        })
        program = fuzzer.generate_program()
        self._save_ir("layer1234_with_transaction", program)

    def test_layer_12345_full_pipeline(self):
        fuzzer = IRFuzzer(SCHEMA_PATH, config={
            "enable_onupgradeneeded": True,
            "enable_onsuccess": True,
            "enable_transaction": True,
            "enable_store_ops": True
        })
        program = fuzzer.generate_program()
        self._save_ir("layer12345_full_pipeline", program)

if __name__ == '__main__':
    unittest.main()
