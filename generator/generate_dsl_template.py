# ✅ generator/generate_dsl_template.py
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
        "database": {
            "open": {
                "name": "testDB",
                "version": 1,
                "onupgradeneeded": {
                    "createObjectStore": [
                        {
                            "name": "store1",
                            "options": {
                                "keyPath": "id",
                                "autoIncrement": True
                            }
                        }
                    ]
                },
                "onsuccess": {
                    "assign": { "db": "result" }
                }
            }
        },
        "transactions": [
            {
                "from": "db",
                "stores": ["store1"],
                "mode": "readwrite",
                "assign": { "tx": "result" }
            }
        ],
        "operations": [
            {
                "type": "put",
                "from": "tx",
                "store": "store1",
                "value": { "id": 1, "name": "Alice" }
            },
            {
                "type": "get",
                "from": "tx",
                "store": "store1",
                "key": 1
            }
        ]
    }

    return dsl

if __name__ == "__main__":
    schema_path = os.path.join("../schema", "indexeddb_schema.json")
    output_file = "test_dsl.json"

    dsl = generate_dsl_template(schema_path)

    with open(output_file, "w") as f:
        json.dump(dsl, f, indent=2)

    print(f"\u2705 DSL template saved to {output_file}")