import json
import os

def get_dummy_value(param_type):
    return {
        "string": "example_string",
        "number": 1,
        "boolean": True,
        "any": "any_value",
        "array": ["item1", "item2"],
        "object": { "key": "value" }
    }.get(param_type, "unknown")

def generate_dsl_template(schema_path: str) -> dict:
    with open(schema_path, "r") as f:
        schema = json.load(f)

    dsl = {
        "database": {},
        "transactions": [],
        "operations": []
    }

    # 1. open
    open_api = schema["database"]["open"]
    open_dsl = {}
    for param in open_api["params"]:
        open_dsl[param["name"]] = get_dummy_value(param["type"])
    open_dsl["onsuccess"] = { "assign": { "db": "result" } }
    dsl["database"]["open"] = open_dsl

    # 2. transaction
    tx_api = schema["transaction"]["create"]
    tx_dsl = {
        "from": "db",
        "stores": ["store1"],
        "mode": "readwrite",
        "assign": { "tx": "result" }
    }
    dsl["transactions"].append(tx_dsl)

    # 3. operation 示例
    for op_name in ["put", "get"]:
        op_def = schema["storeOperations"][op_name]
        op_entry = {
            "type": op_name,
            "from": "tx",
            "store": "store1"
        }
        for param in op_def["params"]:
            if param["name"] not in op_entry:
                op_entry[param["name"]] = get_dummy_value(param["type"])
        dsl["operations"].append(op_entry)

    return dsl
import pathlib

# ✅ 入口函数：生成 JSON 文件
if __name__ == "__main__":
    schema_file = os.path.join("../schema", "indexeddb_schema.json")

    dsl = generate_dsl_template(schema_file)

    output_file = pathlib.Path("test_dsl.json").resolve()
    with open(output_file, "w") as f:
        json.dump(dsl, f, indent=2)

    print(f"✅ DSL 模板已保存到：{output_file}")
