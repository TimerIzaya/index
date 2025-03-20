import json
import random
from random import choice

import config
from IR.IRType import Type


class IndexedDBSchemaParser:
    """
    基于嵌套结构的 IndexedDB schema 解析器：
    每个接口包含：
    - staticMethods
    - instanceMethods
    - instanceProperties
    - events
    """
    def __init__(self, schema_file=config.SCHEMA_FILE):
        with open(schema_file, "r") as f:
            self.schema = json.load(f)

    def get_interfaces(self):
        return list(self.schema.keys())

    def get_static_methods(self, interface):
        return self.schema.get(interface, {}).get("staticMethods", {})

    def get_instance_methods(self, interface):
        return self.schema.get(interface, {}).get("instanceMethods", {})

    def get_properties(self, interface):
        props = self.schema.get(interface, {}).get("instanceProperties", [])
        return {p['name']: p for p in props if 'name' in p}

    def get_events(self, interface):
        return self.schema.get(interface, {}).get("events", [])

    def get_exceptions(self, interface, method):
        return self.get_instance_methods(interface).get(method, {}).get("exceptions", [])

    def get_parameters(self, interface, method):
        return self.get_instance_methods(interface).get(method, {}).get("parameters", [])

    def get_return_type(self, interface, method):
        return self.get_instance_methods(interface).get(method, {}).get("returns", None)

    def extract_param_type_from_schema(self, param):
        """返回一个 Type 对象用于后续调用"""
        typeInfo = param.get("type", {})
        maybe = [typeInfo]
        selected = random.choices(maybe)
        return Type(selected)


class IRTypeRegistry:
    def __init__(self):
        self.known_types = set()
        self.collect_types_from_schema()
        config.AllIRTypes.append(self.known_types)

    def collect_types_from_schema(self):
        parser = IndexedDBSchemaParser()
        for iface in parser.get_interfaces():
            for method_dict in [parser.get_static_methods(iface), parser.get_instance_methods(iface)]:
                for method in method_dict.values():
                    for param in method.get("params", []):
                        raw_type = param.get("type", {})
                        if isinstance(raw_type, list):
                            for entry in raw_type:
                                self.known_types.add(Type(entry.get(config.Consts.TypeName, "any")))
                        else:
                            self.known_types.add(Type(raw_type.get(config.Consts.TypeName, "any")))

if __name__ == "__main__":
        parser = IndexedDBSchemaParser()
        apiName = parser.get_interfaces()[0]
        mes = parser.get_static_methods(apiName).items()
        for me in mes:
            params = parser.get_parameters(apiName, me)
            for p in params:
                t = parser.extract_param_type_from_schema(p)
                print(1)
