from typing import List, Optional, Dict, Union

# ================= InterfaceInfo =================
# Schema 片段:
# {
#   "IDBDatabase": {
#     "category": "interface",
#     "inherits": ["EventTarget"],
#     "staticMethods": { ... },
#     "instanceMethods": { ... },
#     "instanceProperties": [...],
#     "events": [...],
#     "exceptions": [...]
#   }
# }
class InterfaceInfo:
    def __init__(self, name: str, definition: dict):
        self.name = name
        self.category = definition.get("category")
        self.inherits = definition.get("inherits", [])
        self.static_methods = definition.get("staticMethods", {})
        self.instance_methods = definition.get("instanceMethods", {})
        self.properties = definition.get("instanceProperties", [])
        self.events = definition.get("events", [])
        self.exceptions = definition.get("exceptions", [])


# ================= MethodInfo =================
# Schema 片段:
# "transaction": {
#   "params": [...],
#   "returns": {"typename": "IDBTransaction"},
#   "exceptions": [...],
#   "isConstructor": false,
#   "kind": "method"
# }
class MethodInfo:
    def __init__(self, name: str, definition: dict, is_static: bool = False):
        self.name = name
        self.params = definition.get("params", [])
        self.returns = definition.get("returns")
        self.exceptions = definition.get("exceptions", [])
        self.is_constructor = definition.get("isConstructor", False)
        self.kind = definition.get("kind", "method")
        self.is_static = is_static


# ================= ParamInfo =================
# Schema 片段:
# {
#   "name": "storeNames",
#   "type": [
#     {"typename": "string"},
#     {"typename": "array", "items": [{"type": "string"}]}
#   ],
#   "optional": true
# }
class ParamInfo:
    def __init__(self, param: dict):
        self.name = param.get("name")
        self.type = param.get("type")
        self.optional = param.get("optional", False)
        self.default = param.get("default")
        self.enum = param.get("enum")
        self.properties = param.get("properties")  # for object types


# ================= PropertyInfo =================
# Schema 片段:
# "name": "direction",
# "type": {
#     "typename": "string"
# },
# "readonly": true,
# "enum": [
#     "next",
#     "nextunique",
#     "prev",
#     "prevunique"
# ]
class PropertyInfo:
    def __init__(self, prop: dict):
        self.name = prop.get("name")
        self.type = prop.get("type")
        self.readonly = prop.get("readonly", False)
        self.enum = prop.get("enum")
        self.default = prop.get("default")


# ================= EventInfo =================
# Schema 片段:
# {
#   "name": "versionchange",
#   "definedOn": "IDBDatabase",
#   "bubblesFrom": ["IDBFactory"]
# }
class EventInfo:
    def __init__(self, event: dict):
        self.name = event.get("name")
        self.defined_on = event.get("definedOn")
        self.bubbles_from = event.get("bubblesFrom", [])


# ================= ExceptionInfo =================
# Schema 片段:
# "exceptions": ["InvalidStateError", "TransactionInactiveError"]
class ExceptionInfo:
    def __init__(self, name: str):
        self.name = name


# ================= ReturnInfo =================
# Schema 片段:
# "returns": {"typename": "Promise"},
# "returnGeneric": {"typename": "IDatabaseList"}
class ReturnInfo:
    def __init__(self, method_def: dict):
        # 处理 returns 是字符串的情况（主流）
        raw_returns = method_def.get("returns")
        self.typename = raw_returns if isinstance(raw_returns, str) else None

        # 处理 returnGeneric 是字符串
        raw_generic = method_def.get("returnGeneric")
        self.generic = raw_generic if isinstance(raw_generic, str) else None
