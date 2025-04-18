from enum import nonmember

from config import GlobalIRTypeRegistry
from schema.SchemaInstanceTree import initialize_interfaces, ALL_INTERFACES

_parser_instance = None
def get_parser():
    global _parser_instance
    if _parser_instance is None:
        _parser_instance = IndexedDBSchemaParser()
        _parser_instance.load()
    return _parser_instance

class SchemaNode:
    def __init__(self, node):
        self.node = node

    def getStaticMethod(self, name: str):
        method = getattr(self.node, "staticMethods", {}).get(name)
        return SchemaNode(method) if method else None

    def getInstanceMethod(self, name: str):
        method = getattr(self.node, "instanceMethods", {}).get(name)
        return SchemaNode(method) if method else None

    def getEvent(self, name: str):
        for evt in getattr(self.node, "events", []):
            if evt.name == name:
                return evt
        return None

    def getProperty(self, name: str):
        for p in getattr(self.node, "instanceProperties", []):
            if p.name == name:
                return p
        return None

    def getParam(self, index: int):
        params = getattr(self.node, "params", [])
        if 0 <= index < len(params):
            return SchemaNode(params[index])
        return None

    def getParams(self):
        params = getattr(self.node, "params", [])
        return SchemaNode(params)

    def getReturn(self):
        return SchemaNode(getattr(self.node, "returns", None)) if hasattr(self.node, "returns") else None

    def getAttr(self, key: str):
        if isinstance(self.node, dict):
            return self.node.get(key)
        return getattr(self.node, key, None)

    def raw(self):
        return self.node


class IndexedDBSchemaParser:
    def __init__(self):
        self.root = {}

    def load(self):
        initialize_interfaces()
        self.root = {name: SchemaNode(iface) for name, iface in ALL_INTERFACES.items()}
        self.populate_all_types_from_parser()

    def getInterface(self, name: str):
         return self.root.get(name)

    def populate_all_types_from_parser(self):
        def visit(node: SchemaNode):
            if not node:
                return
            raw = node.raw()
            if isinstance(raw, dict):
                for k, v in raw.items():
                    if k == "typename" and isinstance(v, str):
                        GlobalIRTypeRegistry.register(v)
                    visit(SchemaNode(v))
            elif isinstance(raw, list):
                for item in raw:
                    visit(SchemaNode(item))
            elif hasattr(raw, "__dict__"):
                for attr in vars(raw).values():
                    visit(SchemaNode(attr))

        for schema_node in self.root.values():
            visit(schema_node)


SchemaParser = get_parser()


if __name__ == '__main__':
    parser = IndexedDBSchemaParser()
    parser.load()

    # 获取 open 方法的第一个参数类型
    t1 = parser.getInterface("IDBFactory") \
        .getStaticMethod("open") \
        .getParam(0) \
        .getAttr("type")

    # 获取 transaction 方法第一个参数（联合类型）
    t2 = parser.getInterface("IDBDatabase") \
        .getInstanceMethod("transaction") \
        .getParam(0) \
        .getAttr("type")

    # 获取 onversionchange 事件定义
    e1 = parser.getInterface("IDBDatabase") \

    # 获取 put() 的返回类型
    ret = parser.getInterface("IDBObjectStore") \
        .getInstanceMethod("put") \
        .getReturn() \
        .getAttr("typename")

