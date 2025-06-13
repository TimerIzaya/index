import random
from typing import Union

from IR.type.IDBType import IDBType
from schema.SchemaClass import TypeInfo, MethodInfo


class IDBTypeTool:

    @staticmethod
    def normalTypeinfo(typeInfo: Union[TypeInfo, list]) -> TypeInfo:
        if isinstance(typeInfo, list):
            return random.choice(typeInfo)
        return typeInfo

    @staticmethod
    def extractIDBTypeFromMethodReturns(m: MethodInfo) -> IDBType:
        if isinstance(m.returns, list):
            # 可能有多个返回类型的场景
            return random.choice(m.returns).typename

        return m.returns.typename
