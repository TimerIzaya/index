import json
import config

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

if __name__ == "__main__":
    parser = IndexedDBSchemaParser()
    interfaces = parser.get_interfaces()
    print("Available Interfaces:", interfaces)

    for interface in interfaces:
        print(f"\n===== Interface: {interface} =====")
        print("Static Methods:", list(parser.get_static_methods(interface).keys()))
        print("Instance Methods:", list(parser.get_instance_methods(interface).keys()))
        print("Properties:", list(parser.get_properties(interface).keys()))
        print("Events:", [e['name'] for e in parser.get_events(interface)])
        for method in parser.get_instance_methods(interface):
            print(f"\n  --- Method: {method} ---")
            print("  Exceptions:", parser.get_exceptions(interface, method))
            print("  Parameters:", parser.get_parameters(interface, method))
            print("  Return Type:", parser.get_return_type(interface, method))