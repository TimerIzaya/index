import random
from typing import Optional

from IR import IRContext
from IR.IRNodes import Literal, Identifier
from config import OPTIONAL_JUMP
from schema.SchemaClass import ParamInfo, TypeInfo


class ParameterGenerator:
    def __init__(self, context: IRContext):
        self.context = context

    def generate_parameter(self, param: ParamInfo):
        # 处理 optional 参数：50% 概率跳过
        if param.optional and random.random() < 0.5:
            return Literal(OPTIONAL_JUMP)

        # 处理 enum 参数：直接从枚举中随机选择一个
        if param.enum:
            return Literal(random.choice(param.enum))

        # 获得type，有些可以是string 也可以是list string
        # list<string>意思是可以接受多种类型的参数，例如createIndex的keyPath，支持字符串或者字符串数组
        if isinstance(param.type, list):
            type_dict = random.choice(param.type)
        else:
            type_dict = param.type

        # 如果参数是一个object，并且有properties，说明是schema要求的固定类型的object
        # 例如createIndex的options，必须是 { unique?: t/f, multiEntry?: t/f}
        if isinstance(param.type, object) and param.properties is not None:
            # 固定字段组成的对象类型，例如 IDBIndexParameters
            objParam = {}
            for property in param.properties:
                if 'type' not in property:
                    print(1)
                objParam[property.name] = self.generate_parameter(property.type)
            return Literal(objParam)

        typeInfo = TypeInfo(type_dict)

        typename = self._resolve_typename(typeInfo)

        # 优先重用已有变量
        candidates = self.context.get_visible_variables(typename)
        if candidates:
            return random.choice(candidates).identifier  # 返回 Identifier

        # 否则生成 Literal
        value = self.generate_value_from_type(typeInfo)
        return Literal(value)

    def _resolve_typename(self, type_info):
        if isinstance(type_info, list):
            return random.choice(type_info).get("typename", "any")
        elif isinstance(type_info, dict):
            return type_info.get("typename", "any")
        return "any"

    def generate_value_from_type(self, typeinfo: TypeInfo):
        x = typeinfo.typename
        typename = typeinfo.typename or "any"
        items = typeinfo.items

        if typename == "boolean":
            return random.choice([True, False])

        if typename == "number":
            return random.randint(0, 100)

        if typename == "string":
            return "str_" + str(random.randint(0, 9999))

        if typename == "array":
            count = random.randint(1, 5)
            element_type = TypeInfo({"typename": "any"})

            if isinstance(items, list) and len(items) == 1:
                element_type = TypeInfo(items[0])
            elif isinstance(items, dict):
                element_type = TypeInfo(items)

            return [self.generate_value_from_type(element_type) for _ in range(count)]

        if typename == "null":
            return None

        if typename == "any":
            return random.choice(["fallback", 42, True])

        if typename.startswith("IDB") or "Exception" in typename or "Error" in typename:
            return None

        return f"{typename}_instance"
