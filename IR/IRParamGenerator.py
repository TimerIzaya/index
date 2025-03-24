import random
from IR.IRNodes import Literal, Identifier
from IRContext import IRContext
from IRType import Type
from schema.SchemaClass import ParamInfo


class ParameterGenerator:
    def __init__(self, context: IRContext):
        self.context = context

    def generate_parameter(self, param: ParamInfo):
        param_type_info = param.type
        typename = self._resolve_typename(param_type_info)

        # 尝试重用已存在的变量
        candidates = self.context.get_visible_variables(typename)
        if candidates:
            return random.choice(candidates).identifier  # 直接返回 Identifier

        # 否则随机生成 Literal（常量值）
        value = self._generate_value_for_type(typename)
        return Literal(value, type=typename)

    def _resolve_typename(self, type_info):
        if isinstance(type_info, list):
            return random.choice(type_info).get("typename", "any")
        elif isinstance(type_info, dict):
            return type_info.get("typename", "any")
        return "any"

    def _generate_value_for_type(self, typename):
        # ✅ 特殊类型：IDB 开头 或 DOMException/TypeError 等异常类
        if typename.startswith("IDB") or "Exception" in typename or "Error" in typename:
            return None

        # ✅ 基础类型随机值生成
        if typename == "string":
            return "example_" + str(random.randint(1, 100))
        elif typename == "number":
            return random.randint(1, 100)
        elif typename == "boolean":
            return random.choice([True, False])
        elif typename == "array":
            return []
        elif typename == "object":
            return {"key": "value"}
        elif typename == "null":
            return None
        elif typename == "any":
            return random.choice(["fallback", 42, True])
        else:
            # 默认处理（可以是空值、占位对象等）
            return f"{typename}_instance"

