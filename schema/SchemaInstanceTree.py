import json
from typing import Dict

import config
from schema.SchemaClass import *

SCHEMA_FILE = "indexeddb_schema.json"
ALL_INTERFACES: Dict[str, InterfaceInfo] = {}

def load_schema() -> dict:
    with open(config.SCHEMA_FILE, "r") as f:
        return json.load(f)

def build_interface(name: str, data: dict) -> InterfaceInfo:
    iface = InterfaceInfo({"name": name, **data})

    # build static methods
    iface.staticMethods = {}
    for mname, mdef in data.get("staticMethods", {}).items():
        method = build_method(mname, mdef)
        iface.staticMethods[mname] = method

    # build instance methods
    iface.instanceMethods = {}
    for mname, mdef in data.get("instanceMethods", {}).items():
        method = build_method(mname, mdef)
        iface.instanceMethods[mname] = method

    # build instance properties
    iface.instanceProperties = []
    for prop in data.get("instanceProperties", []):
        prop_obj = PropertyInfo(prop)
        iface.instanceProperties.append(prop_obj)

    # build events
    iface.events = [EventInfo(e) for e in data.get("events", [])]

    # build exceptions
    exlist = data.get("exceptions", [])
    iface.exceptions = [ExceptionInfo(e if isinstance(e, dict) else {"name": e}) for e in exlist]

    return iface

def build_method(name: str, mdef: dict) -> MethodInfo:
    method = MethodInfo({"name": name, **mdef})
    method.params = []
    for p in mdef.get("params", []):
        param_obj = ParamInfo(p)
        if "type" in p:
            param_obj.typeInfo = build_type(p["type"])
        method.params.append(param_obj)

    if "returns" in mdef or "returnGeneric" in mdef:
        method.returns = ReturnInfo(mdef)
        if hasattr(method.returns, "typename"):
            method.returns.typeInfo = build_type(method.returns.typename)
        if hasattr(method.returns, "generic"):
            method.returns.genericTypeInfo = build_type(method.returns.generic)
    return method

def build_type(tdef):
    if isinstance(tdef, str):
        return TypeInfo({"typename": tdef})
    elif isinstance(tdef, dict):
        return TypeInfo(tdef)
    elif isinstance(tdef, list):
        return [TypeInfo(t) for t in tdef]
    else:
        return None

def initialize_interfaces():
    global schema
    schema = load_schema()
    for name, data in schema.items():
        ALL_INTERFACES[name] = build_interface(name, data)

def check_unmapped_fields():
    print("[Schema Coverage Check]")
    total = 0
    missing_schema = 0
    extra_inst = 0

    def check(schema_obj, instance_obj, path="root"):
        nonlocal total, missing_schema, extra_inst

        if isinstance(schema_obj, dict):
            schema_keys = set(schema_obj.keys())
            for key in schema_keys:
                total += 1
                has_node = False
                if isinstance(instance_obj, dict):
                    has_node = key in instance_obj
                else:
                    has_node = hasattr(instance_obj, key)

                if not has_node:
                    print(f"[Missing] in instree: {path}.{key}")
                    missing_schema += 1
                else:
                    next_instance = instance_obj[key] if isinstance(instance_obj, dict) else getattr(instance_obj, key, None)
                    check(schema_obj[key], next_instance, f"{path}.{key}")

        elif isinstance(schema_obj, list) and isinstance(instance_obj, list):
            for i, item in enumerate(schema_obj):
                if i < len(instance_obj):
                    check(item, instance_obj[i], f"{path}[{i}]")

    for name, data in schema.items():
        schema_iface = data
        instance_iface = ALL_INTERFACES.get(name)
        if instance_iface:
            check(schema_iface, instance_iface, path=name)

    print(f"Checked {total} schema nodes")
    print(f"Missing nodes: {missing_schema}")
    print(f"Extra field check skipped (fields are optional)")


if __name__ == "__main__":
    initialize_interfaces()
    check_unmapped_fields()
