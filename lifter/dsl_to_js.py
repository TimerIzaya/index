import json

def dsl_to_js(dsl: dict) -> str:
    lines = []

    # Step 1: indexedDB.open
    db_open = dsl.get("database", {}).get("open")
    if db_open:
        db_name = db_open["name"]
        version = db_open.get("version", 1)
        lines.append(f'const request = indexedDB.open("{db_name}", {version});')

        lines.append("request.onsuccess = function(event) {")
        lines.append("  const db = event.target.result;")

        # Step 2: transactions
        for tx in dsl.get("transactions", []):
            store_list = ', '.join(f'"{s}"' for s in tx["stores"])
            mode = tx.get("mode", "readonly")
            lines.append(f'  const tx = db.transaction([{store_list}], "{mode}");')

        # Step 3: operations
        for op in dsl.get("operations", []):
            store = op["store"]
            if op["type"] == "put":
                val = json.dumps(op["value"])
                lines.append(f'  tx.objectStore("{store}").put({val});')
            elif op["type"] == "get":
                key = json.dumps(op["key"])
                lines.append(f'  tx.objectStore("{store}").get({key});')
            elif op["type"] == "delete":
                key = json.dumps(op["key"])
                lines.append(f'  tx.objectStore("{store}").delete({key});')
            elif op["type"] == "clear":
                lines.append(f'  tx.objectStore("{store}").clear();')

        lines.append("};")

    return '\n'.join(lines)

# ✅ 运行主程序
if __name__ == "__main__":
    with open("../generator/test_dsl.json", "r") as f:
        dsl = json.load(f)

    js_code = dsl_to_js(dsl)

    with open("test_output.js", "w") as f:
        f.write(js_code)

    print("✅ JS code saved to test_output.js")
