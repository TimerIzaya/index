import json

def dsl_to_js(dsl: dict) -> str:
    lines = []

    # Step 1: open database
    db_open = dsl.get("database", {}).get("open")
    if db_open:
        db_name = db_open["name"]
        version = db_open.get("version", 1)
        lines.append(f'const request = indexedDB.open("{db_name}", {version});')

        # onupgradeneeded
        if "onupgradeneeded" in db_open:
            lines.append("request.onupgradeneeded = function(event) {")
            lines.append("  const db = event.target.result;")
            for store in db_open["onupgradeneeded"].get("createObjectStore", []):
                store_name = store["name"]
                options = store.get("options", {})
                opt_str = ', '.join([f'{k}: {json.dumps(v)}' for k, v in options.items()])
                lines.append(f'  db.createObjectStore("{store_name}", {{{opt_str}}});')
            lines.append("};")

        # onsuccess
        if "onsuccess" in db_open:
            lines.append("request.onsuccess = function(event) {")
            lines.append("  const db = event.target.result;")

            # Step 2: transactions
            transactions = dsl.get("transactions", [])
            for tx in transactions:
                store_list = ', '.join([f'"{s}"' for s in tx["stores"]])
                tx_mode = tx["mode"]
                lines.append(f'  const tx = db.transaction([{store_list}], "{tx_mode}");')

            # Step 3: operations
            operations = dsl.get("operations", [])
            for op in operations:
                store = op["store"]
                if op["type"] == "put":
                    value = json.dumps(op["value"])
                    lines.append(f'  tx.objectStore("{store}").put({value});')
                elif op["type"] == "get":
                    key = json.dumps(op["key"])
                    lines.append(f'  tx.objectStore("{store}").get({key});')
                elif op["type"] == "delete":
                    key = json.dumps(op["key"])
                    lines.append(f'  tx.objectStore("{store}").delete({key});')

            lines.append("};")  # end of onsuccess

    return '\n'.join(lines)


if __name__ == "__main__":
    with open("test_dsl.json", "r") as f:
        dsl = json.load(f)

    js_code = dsl_to_js(dsl)
    with open("test_output.js", "w") as f:
        f.write(js_code)

    print("✅ JS code written to test_output.js")
