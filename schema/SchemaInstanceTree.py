import json
from typing import Dict, Optional, Union, List

from schema.SchemaClass import InterfaceInfo
from config import SCHEMA_FILE


class SchemaInstanceTree:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SchemaInstanceTree, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.schema_file = SCHEMA_FILE
        self.raw_schema: dict = {}
        self.interfaces: Dict[str, InterfaceInfo] = {}
        self._initialized = True
        self.load()  # ✅ 自动加载

    def load(self):
        if not self.schema_file:
            raise ValueError("Schema file path not set.")
        with open(self.schema_file, "r") as f:
            self.raw_schema = json.load(f)
        for name, data in self.raw_schema.items():
            self.interfaces[name] = self._build_interface(name, data)

    def _build_interface(self, name: str, data: dict) -> InterfaceInfo:
        interface_dict = {
            "category": data.get("category"),
            "events": data.get("events", []),
            "inherits": data.get("inherits"),
            "instanceMethods": list(data.get("instanceMethods", {}).values()),
            "instanceProperties": data.get("instanceProperties", []),
            "staticMethods": list(data.get("staticMethods", {}).values()),
            "staticProperties": data.get("staticProperties", []),
            "name": name,
        }
        return InterfaceInfo(interface_dict)

    def get_interface(self, name: str) -> Optional[InterfaceInfo]:
        return self.interfaces.get(name)

    def summary(self):
        print(f"[SchemaInstanceTree] Loaded {len(self.interfaces)} interfaces:")
        for name in self.interfaces:
            print(f"  - {name}")

    def check_coverage(self):
        print("[Schema Coverage Check]")
        total, missing = 0, 0

        def check(schema_node, instance_node, path="root"):
            nonlocal total, missing
            if isinstance(schema_node, dict):
                for key in schema_node:
                    total += 1
                    has_attr = isinstance(instance_node, dict) and key in instance_node or hasattr(instance_node, key)
                    if not has_attr:
                        print(f"[Missing] {path}.{key}")
                        missing += 1
                    else:
                        next_inst = (
                            instance_node[key] if isinstance(instance_node, dict)
                            else getattr(instance_node, key)
                        )
                        check(schema_node[key], next_inst, f"{path}.{key}")
            elif isinstance(schema_node, list) and isinstance(instance_node, list):
                for i, item in enumerate(schema_node):
                    if i < len(instance_node):
                        check(item, instance_node[i], f"{path}[{i}]")

        for name, schema_iface in self.raw_schema.items():
            inst = self.interfaces.get(name)
            if inst:
                check(schema_iface, inst, path=name)

        print(f"Total nodes checked: {total}")
        print(f"Missing nodes: {missing}")
