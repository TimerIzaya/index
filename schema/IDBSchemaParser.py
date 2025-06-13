from typing import Union

class SchemaNode:
    def __init__(self, node):
        self.node = node

    def __getattr__(self, name):
        return getattr(self.node, name)

    def _wrap(self, val):
        return SchemaNode(val) if val is not None else None

    def getStaticMethod(self, name: str):
        return self._wrap(getattr(self.node, "staticMethods", {}).get(name))

    def getInstanceMethod(self, name: str):
        return self._wrap(getattr(self.node, "instanceMethods", {}).get(name))

    def getEvent(self, name: str):
        return self._wrap(next((e for e in getattr(self.node, "events", []) if e.name == name), None))

    def getProperty(self, name: str):
        return self._wrap(next((p for p in getattr(self.node, "instanceProperties", []) if p.name == name), None))

    def getParam(self, name: Union[str, int]):
        params = getattr(self.node, "params", [])
        if isinstance(name, int) and 0 <= name < len(params):
            return self._wrap(params[name])
        elif isinstance(name, str):
            return self._wrap(next((p for p in params if getattr(p, "name", None) == name), None))
        return None

    def getParams(self):
        return self._wrap(getattr(self.node, "params", []))

    def getReturn(self):
        return self._wrap(getattr(self.node, "returns", None))

    def getType(self):
        return self._wrap(getattr(self.node, "type", None))

    def getTypename(self):
        t = getattr(self.node, "type", None)
        if hasattr(t, "typename"):
            return t.typename
        return None

    def getAttr(self, key: str):
        if isinstance(self.node, dict):
            return self.node.get(key)
        return getattr(self.node, key, None)

    def raw(self):
        return self.node


class IDBSchemaParser:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.root = {}
        self._initialized = True
        self._load()

    def _load(self):
        from schema.SchemaInstanceTree import SchemaInstanceTree
        schema_tree = SchemaInstanceTree()
        iface_map = schema_tree.interfaces
        self.root = {name: SchemaNode(iface) for name, iface in iface_map.items()}
        self._populate_all_types_from_parser()

    def _populate_all_types_from_parser(self):
        visited = set()

        def visit(node: SchemaNode):
            if not node:
                return
            raw = node.raw()
            if id(raw) in visited:
                return
            visited.add(id(raw))

            if isinstance(raw, dict):
                for k, v in raw.items():
                    # if k == "typename" and isinstance(v, str):
                    #     GlobalIRTypeRegistry.register(v)
                    visit(SchemaNode(v))
            elif isinstance(raw, list):
                for item in raw:
                    visit(SchemaNode(item))
            elif hasattr(raw, "__dict__"):
                for attr in vars(raw).values():
                    visit(SchemaNode(attr))

        for schema_node in self.root.values():
            visit(schema_node)

    def _get_interface(self, name: str):
        return self.root.get(name)

    @classmethod
    def _get_instance(cls) -> "IDBSchemaParser":
        if cls._instance is None:
            cls._instance = IDBSchemaParser()
        return cls._instance

    @classmethod
    def getInterface(cls, name: str) -> SchemaNode:
        return cls._get_instance()._get_interface(name)



