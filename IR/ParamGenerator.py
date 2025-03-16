import random

class ParameterGenerator:
    """
    基于 IndexedDB schema 字段生成参数值的工具类
    用于 fuzzing 时自动构造合法或边界测试参数
    """

    def __init__(self):
        pass

    def generate_parameter(self, param_info):
        name = param_info.get("name")
        type_ = param_info.get("type")
        optional = param_info.get("optional", False)

        if optional and random.random() < 0.3:
            return None

        return self._generate_by_type(type_)

    def _generate_by_type(self, type_):
        if type_ in ("DOMString", "string"):
            return random.choice(["store1", "user", "example", ""])

        if type_ in ("unsigned long", "unsigned long long", "int", "number"):
            return random.randint(0, 10000)

        if type_ == "boolean":
            return random.choice([True, False])

        if type_ == "DOMStringList":
            return ["store1", "store2", "data"]

        if type_ == "object":
            return {"key": "value", "flag": True}

        if type_ == "any":
            return random.choice(["string", 123, True, None, {}, []])

        if type_ == "IDBTransactionMode":
            return random.choice(["readonly", "readwrite", "versionchange"])

        if type_ == "IDBKeyRange":
            return {"lower": 1, "upper": 10}

        return f"<Unresolved:{type_}>"

    def generate_arguments(self, param_list):
        return [self.generate_parameter(param) for param in param_list]

if __name__ == '__main__':
    gen = ParameterGenerator()
    args = gen.generate_arguments([
        {"name": "storeNames", "type": "DOMStringList"},
        {"name": "mode", "type": "IDBTransactionMode", "optional": True}
    ])
    print(args)
