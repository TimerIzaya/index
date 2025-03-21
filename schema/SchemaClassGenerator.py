import json
from pathlib import Path
from collections import defaultdict

import config
SCHEMA_FILE = config.SCHEMA_FILE
OUTPUT_FILE = "SchemaClass.py"

# 目标节点名称
TARGET_CLASSES = [
    "InterfaceInfo", "MethodInfo", "ParamInfo", "TypeInfo",
    "PropertyInfo", "EventInfo", "ExceptionInfo", "ReturnInfo"
]

# 每类结构对应路径规则和字段累积器
field_map = defaultdict(set)

def collect_interface_info(schema):
    for iface_name, iface_def in schema.items():
        field_map["InterfaceInfo"].update(iface_def.keys())
        if "staticMethods" in iface_def:
            for name, method in iface_def["staticMethods"].items():
                field_map["MethodInfo"].update(method.keys())
                if "params" in method:
                    for param in method["params"]:
                        field_map["ParamInfo"].update(param.keys())
                        if "type" in param:
                            collect_type(param["type"])
                if "returns" in method or "returnGeneric" in method:
                    field_map["ReturnInfo"].add("returns")
                    if "returnGeneric" in method:
                        field_map["ReturnInfo"].add("returnGeneric")
        if "instanceMethods" in iface_def:
            for name, method in iface_def["instanceMethods"].items():
                field_map["MethodInfo"].update(method.keys())
                if "params" in method:
                    for param in method["params"]:
                        field_map["ParamInfo"].update(param.keys())
                        if "type" in param:
                            collect_type(param["type"])
                if "returns" in method or "returnGeneric" in method:
                    field_map["ReturnInfo"].add("returns")
                    if "returnGeneric" in method:
                        field_map["ReturnInfo"].add("returnGeneric")
        if "instanceProperties" in iface_def:
            for prop in iface_def["instanceProperties"]:
                field_map["PropertyInfo"].update(prop.keys())
                if "type" in prop:
                    collect_type(prop["type"])
        if "events" in iface_def:
            for ev in iface_def["events"]:
                field_map["EventInfo"].update(ev.keys())
        if "exceptions" in iface_def:
            for ex in iface_def["exceptions"]:
                if isinstance(ex, dict):
                    field_map["ExceptionInfo"].update(ex.keys())
                else:
                    field_map["ExceptionInfo"].add("name")

def collect_type(t):
    if isinstance(t, list):
        for item in t:
            field_map["TypeInfo"].update(item.keys())
    elif isinstance(t, dict):
        field_map["TypeInfo"].update(t.keys())


def generate_class_code(classname: str, fields: set) -> str:
    lines = [f"class {classname}:", "    def __init__(self, data: dict):"]
    if not fields:
        lines.append("        pass")
    else:
        for f in sorted(fields):
            lines.append(f"        self.{f} = data.get(\"{f}\")")
    return "\n".join(lines)


def main():
    with open(SCHEMA_FILE, "r") as f:
        schema = json.load(f)

    collect_interface_info(schema)

    class_defs = ["from typing import List, Optional, Dict\n"]
    for cls in TARGET_CLASSES:
        class_defs.append(f"# ========== {cls} ==========")
        class_defs.append(generate_class_code(cls, field_map[cls]))
        class_defs.append("")

    Path(OUTPUT_FILE).write_text("\n".join(class_defs))
    print(f"✅ Generated {OUTPUT_FILE} with {len(TARGET_CLASSES)} classes.")

if __name__ == '__main__':
    main()
