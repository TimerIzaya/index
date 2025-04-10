import random

from IR import IRContext
from IR.IRNodes import Literal, Identifier
from config import OPTIONAL_JUMP
from schema.SchemaClass import ParamInfo


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

        # 正常流程
        param_type_info = param.type
        typename = self._resolve_typename(param_type_info)

        # 优先重用已有变量
        candidates = self.context.get_visible_variables(typename)
        if candidates:
            return random.choice(candidates).identifier  # 返回 Identifier

        # 否则生成 Literal
        value = self.generate_value_from_typename(typename)
        return Literal(value)

    def _resolve_typename(self, type_info):
        if isinstance(type_info, list):
            return random.choice(type_info).get("typename", "any")
        elif isinstance(type_info, dict):
            return type_info.get("typename", "any")
        return "any"

    def generate_value_from_typename(self, typename):
        # ✅ 特殊类型：IDB 开头 或 DOMException/TypeError 等异常类
        if typename.startswith("IDB") or "Exception" in typename or "Error" in typename:
            return None

        # ✅ 基础类型随机值生成
        if typename == "string":
            return "v_" + str(random.randint(1, 100))
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

