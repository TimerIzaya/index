import random
from typing import Optional, Union

from IR import IRContext
from IR.IRNodes import Literal, Identifier
from config import OPTIONAL_JUMP
from schema.SchemaClass import ParamInfo, TypeInfo, IDBType


class ParameterGenerator:
    def __init__(self, context: IRContext):
        self.context = context

    def generate_parameter(self, param: ParamInfo):
        if not isinstance(param, ParamInfo):
            raise TypeError("generate_parameter 的入参必须是 ParamInfo 类型")

        """
        根据给定的 ParamInfo 对象生成一个合适的参数值，
        支持 optional、enum、固定结构对象 和 基本类型等情形。
        """
        # 如果参数是 optional 类型，则有 50% 的概率跳过
        if param.optional and random.random() < 0.5:
            return Literal(OPTIONAL_JUMP)

        # 如果参数是一个枚举值，则从枚举列表中随机选择一个作为参数
        if param.enum:
            return Literal(random.choice(param.enum))

        # 如果参数是一个具有固定属性的 object 类型（如 IDBIndexParameters）
        if isinstance(param.type, object) and param.properties is not None:
            objParam = {}
            for prop in param.properties:
                # 对每个属性递归生成其值
                objParam[prop.name] = self.generate_value_from_type(prop.type)
            return Literal(objParam)

        # 参数类型可能是 TypeInfo 或 List[TypeInfo]，统一解析为一个 TypeInfo 实例
        typeInfoUnion = param.type
        typeInfo = self._resolve_typeinfo(typeInfoUnion)

        # 优先使用当前上下文中已存在的变量（重用）
        typename = typeInfo.typename
        candidates = self.context.get_visible_variables(typename)
        if candidates:
            return random.choice(candidates).identifier  # 返回 Identifier

        # 如果没有可复用变量，生成新的字面量值
        value = self.generate_value_from_type(typeInfo)
        return Literal(value)


    def _resolve_typeinfo(self, typeinfo_union: Union[TypeInfo, list]) -> TypeInfo:
        if isinstance(typeinfo_union, list):
            return random.choice(typeinfo_union)
        return typeinfo_union


    def generate_value_from_type(self, typeinfo: TypeInfo):
        typename = typeinfo.typename
        items = typeinfo.items

        if typename == IDBType.Boolean:
            return random.choice([True, False])

        if typename == IDBType.Number:
            return random.randint(0, 100)

        if typename == IDBType.String:
            return "str_" + str(random.randint(0, 9999))

        if typename == IDBType.Array:
            count = random.randint(1, 5)
            element_type = TypeInfo({"typename": "any"})  # 默认元素类型

            if isinstance(items, list) and len(items) == 1:
                element_type = items[0]
            elif isinstance(items, list) and len(items) > 1:
                element_type = random.choice(items)

            return [self.generate_value_from_type(element_type) for _ in range(count)]

        if typename == IDBType.Null:
            return None

        if typename == IDBType.Any:
            return random.choice(["fallback", 42, True])

        if isinstance(typename, IDBType) and (
            typename.name.startswith("IDB") or "Exception" in typename.name or "Error" in typename.name
        ):
            return None

        return f"{typename.name if isinstance(typename, IDBType) else typename}_instance"
