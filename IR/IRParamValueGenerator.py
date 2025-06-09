import random
from typing import Optional, Union, List

from IR.IRNodes import Literal
from IR.layers.Globals import Global
from config import OPTIONAL_JUMP
from schema.SchemaClass import ParamInfo, TypeInfo, IDBType, MethodInfo


class IRParamValueGenerator:

    @staticmethod
    def generateMethodArgs(method: MethodInfo) -> List[ParamInfo]:
        params = method.params
        args = []
        for param in params:
            args.append(IRParamValueGenerator.generateValueByParamInfo(param))

        if method.name == "createIndex":
            if len(params) >= 3:
                keyPath = args[1]
                options = args[2]
                if isinstance(keyPath, Literal) and isinstance(keyPath.value, list):
                    if isinstance(options, Literal) and isinstance(options.value, dict):
                        if options.value.get("multiEntry", True):
                            options.value["multiEntry"] = False

        return args


    @staticmethod
    def resolveTypeinfo(typeinfo_union: Union[TypeInfo, list]) -> TypeInfo:
        if isinstance(typeinfo_union, list):
            return random.choice(typeinfo_union)
        return typeinfo_union

    @staticmethod
    def generateValueFromType(typeinfo: TypeInfo):
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

            return [IRParamValueGenerator.generateValueFromType(element_type) for _ in range(count)]

        if typename == IDBType.Null:
            return None

        if typename == IDBType.Any:
            return random.choice(["fallback", 42, True])

        if isinstance(typename, IDBType) and (
            typename.name.startswith("IDB") or "Exception" in typename.name or "Error" in typename.name
        ):
            return None

        if typename == IDBType.IDBIndex.value:
            return Global.idbctx.pick_random_index() or "idx_default"
        if typename == IDBType.IDBObjectStore.value:
            return Global.idbctx.get_current_store() or "store_default"
        elif typename == IDBType.IDBKeyRange.value:
            args.append(Literal(f"IDBKeyRange.only({key})"))
        elif typename == IDBType.IDBRequest.value:
            ident = Global.irctx.get_random_identifier(IDBType.IDBRequest.value)
            args.append(ident or Literal("<request>"))
        else:
            # 使用统一生成器处理剩余所有普通类型
            args.append(Literal(valgen.generate(typename, key=key)))

        return f"{typename.name if isinstance(typename, IDBType) else typename}_instance"

    @staticmethod
    def generateValueByParamInfo(param: ParamInfo):
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
                objParam[prop.name] = IRParamValueGenerator.generateValueFromType(prop.type)
            return Literal(objParam)

        # 参数类型可能是 TypeInfo 或 List[TypeInfo]，统一解析为一个 TypeInfo 实例
        typeInfoUnion = param.type
        typeInfo = IRParamValueGenerator.resolveTypeinfo(typeInfoUnion)

        # 优先使用当前上下文中已存在的变量（重用）
        typename = typeInfo.typename
        candidates = Global.irctx.get_visible_variables(typename)
        if candidates:
            return random.choice(candidates).identifier  # 返回 Identifier

        # 如果没有可复用变量，生成新的字面量值
        value = IRParamValueGenerator.generateValueFromType(typeInfo)
        return Literal(value)