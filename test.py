import json

dsl = {
    "hello": "world"
}

with open("test_write.json", "w") as f:
    json.dump(dsl, f, indent=2)

print("✅ test_write.json written")
