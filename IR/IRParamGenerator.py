import random
from typing import Optional

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
        value = self.generate_value_from_typename(typename, param)
        return Literal(value)

    def _resolve_typename(self, type_info):
        if isinstance(type_info, list):
            return random.choice(type_info).get("typename", "any")
        elif isinstance(type_info, dict):
            return type_info.get("typename", "any")
        return "any"

    def generate_value_from_typename(self, typename: str, param: Optional[ParamInfo] = None):
        if typename == "boolean":
            return random.choice([True, False])
        if typename == "number":
            return random.randint(0, 100)
        if typename == "string":
            return "str_" + str(random.randint(0, 9999))
        if typename == "array":
            return []
        if typename == "object" and param and param.properties:
            obj = {}
            for prop in param.properties:
                sub_type = self._resolve_typename(prop["type"])
                if sub_type == "boolean":
                    obj[prop["name"]] = random.choice([True, False])
                elif sub_type == "number":
                    obj[prop["name"]] = random.randint(0, 100)
                elif sub_type == "string":
                    obj[prop["name"]] = "str_" + str(random.randint(0, 9999))
            return obj
        if typename == "null":
            return None
        if typename == "any":
            return random.choice(["fallback", 42, True])
        if typename.startswith("IDB") or "Exception" in typename or "Error" in typename:
            return None

        # 默认 fallback
        return f"{typename}_instance"

