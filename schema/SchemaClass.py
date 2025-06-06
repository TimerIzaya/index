from typing import Optional, List, Dict, Union
from enum import Enum


# ========== IDBType Enum ==========
class IDBType(Enum):
    DOMException = "DOMException"
    DOMStringList = "DOMStringList"
    IDBCursor = "IDBCursor"
    IDBDatabase = "IDBDatabase"
    IDBIndex = "IDBIndex"
    IDBKeyRange = "IDBKeyRange"
    IDBObjectStore = "IDBObjectStore"
    IDBOpenDBRequest = "IDBOpenDBRequest"
    IDBRequest = "IDBRequest"
    IDBTransaction = "IDBTransaction"
    Promise = "Promise"
    TypeError = "TypeError"
    Any = "any"
    Array = "array"
    Boolean = "boolean"
    Function = "function"
    Null = "null"
    Number = "number"
    Object = "object"
    String = "string"
    Void = "void"


# ========== TypeInfo ==========
class TypeInfo:
    typename: IDBType
    items: Optional[List['TypeInfo']]

    def __init__(self, data: Union[str, dict]):
        if isinstance(data, str):
            self.typename = self._resolve_typename(data)
            self.items = None
        elif isinstance(data, dict):
            self.typename = self._resolve_typename(data.get("typename"))
            items_data = data.get("items")
            if isinstance(items_data, list):
                self.items = [TypeInfo(i) for i in items_data]
            elif isinstance(items_data, dict):
                self.items = [TypeInfo(items_data)]
            else:
                self.items = None
        else:
            raise TypeError(f"Invalid type for TypeInfo: {type(data)}")

    def _resolve_typename(self, typename: Optional[str]) -> IDBType:
        if not isinstance(typename, str):
            raise ValueError("typename must be a string")
        try:
            return IDBType(typename)
        except ValueError:
            raise ValueError(f"Unknown typename: '{typename}' not found in IDBType enum")

    def is_enum(self) -> bool:
        return True  # 因为 typename 必然是枚举了

    def __repr__(self):
        return f"TypeInfo(typename={self.typename}, items={self.items})"

# ========== ParamInfo ==========
class ParamInfo:
    name: str
    optional: bool
    enum: Optional[List[str]]
    default: Optional[str]
    properties: Optional[List['PropertyInfo']]
    type: Union[TypeInfo, List[TypeInfo], None]

    def __init__(self, data: dict):
        self.name = data.get("name")
        self.optional = data.get("optional")
        self.enum = data.get("enum")
        self.default = data.get("default")
        self.properties = [PropertyInfo(p) for p in data.get("properties", [])] if "properties" in data else None

        if "type" in data:
            if isinstance(data["type"], list):
                self.type = [TypeInfo(t) for t in data["type"]]
            else:
                self.type = TypeInfo(data["type"])
        else:
            self.type = None


# ========== ReturnInfo ==========
class ReturnInfo:
    returnGeneric: Optional[str]
    returns: Union[TypeInfo, List[TypeInfo], None]

    def __init__(self, data: dict):
        self.returnGeneric = data.get("returnGeneric")
        if "returns" in data:
            if isinstance(data["returns"], list):
                self.returns = [TypeInfo(t) for t in data["returns"]]
            else:
                self.returns = TypeInfo(data["returns"])
        else:
            self.returns = None


# ========== MethodInfo ==========
class MethodInfo:
    name: str
    definedOn: Optional[str]
    isConstructor: bool
    isStatic: bool
    exceptions: Optional[List['ExceptionInfo']]
    returnEnum: Optional[str]
    returnGeneric: Optional[str]
    returns: Union[TypeInfo, List[TypeInfo], None]
    params: List[ParamInfo]

    def __init__(self, data: dict):
        self.name = data.get("name")
        self.definedOn = data.get("definedOn")
        self.isConstructor = data.get("isConstructor", False)
        self.isStatic = data.get("isStatic", False)
        self.exceptions = data.get("exceptions")
        self.returnEnum = data.get("returnEnum")
        self.returnGeneric = data.get("returnGeneric")

        if "returns" in data:
            if isinstance(data["returns"], list):
                self.returns = [TypeInfo(t) for t in data["returns"]]
            else:
                self.returns = TypeInfo(data["returns"])
        else:
            self.returns = None

        self.params = [ParamInfo(p) for p in data.get("params", [])]

    # def genLiteralParams(self):
    #     args = []
    #     for p in self.params:
    #         args.extend(IRParamValueGenerator.generateValueByParamInfo(p))
    #     return args


# ========== PropertyInfo ==========
class PropertyInfo:
    name: str
    readonly: Optional[bool]
    enum: Optional[List[str]]
    default: Optional[str]
    type: Union[TypeInfo, List[TypeInfo], None]

    def __init__(self, data: dict):
        self.name = data.get("name")
        self.readonly = data.get("readonly")
        self.enum = data.get("enum")
        self.default = data.get("default")
        if "type" in data:
            if isinstance(data["type"], list):
                self.type = [TypeInfo(t) for t in data["type"]]
            else:
                self.type = TypeInfo(data["type"])
        else:
            self.type = None


# ========== EventInfo ==========
class EventInfo:
    name: str
    definedOn: Optional[str]
    bubblesFrom: Optional[str]

    def __init__(self, data: dict):
        self.name = data.get("name")
        self.definedOn = data.get("definedOn")
        self.bubblesFrom = data.get("bubblesFrom")


# ========== InterfaceInfo ==========
class InterfaceInfo:
    name: str
    category: Optional[str]
    inherits: Optional[str]
    events: List[EventInfo]
    instanceMethods: Dict[str, MethodInfo]
    staticMethods: Dict[str, MethodInfo]
    instanceProperties: List[PropertyInfo]
    staticProperties: List[PropertyInfo]

    def __init__(self, data: dict):
        self.name = data.get("name")
        self.category = data.get("category")
        self.inherits = data.get("inherits")
        self.events = [EventInfo(e) for e in data.get("events", [])]

        self.instanceMethods = {
            m.get("name", f"method_{i}"): MethodInfo(m)
            for i, m in enumerate(data.get("instanceMethods", []))
        }
        self.staticMethods = {
            m.get("name", f"staticmethod_{i}"): MethodInfo(m)
            for i, m in enumerate(data.get("staticMethods", []))
        }

        self.instanceProperties = [PropertyInfo(p) for p in data.get("instanceProperties", [])]
        self.staticProperties = [PropertyInfo(p) for p in data.get("staticProperties", [])]
