from typing import List, Optional, Dict

# ========== InterfaceInfo ==========
class InterfaceInfo:
    def __init__(self, data: dict):
        self.category = data.get("category")
        self.events: list[EventInfo] = data.get("events")
        self.inherits = data.get("inherits")
        self.instanceMethods = data.get("instanceMethods")
        self.instanceProperties = data.get("instanceProperties")
        self.staticMethods = data.get("staticMethods")

# ========== MethodInfo ==========
class MethodInfo:
    def __init__(self, data: dict):
        self.definedOn = data.get("definedOn")
        self.exceptions = data.get("exceptions")
        self.isConstructor = data.get("isConstructor")
        self.isStatic = data.get("isStatic")
        self.name = data.get("name")
        self.params = data.get("params")
        self.returnEnum = data.get("returnEnum")
        self.returnGeneric = data.get("returnGeneric")
        self.returns = data.get("returns")

# ========== ParamInfo ==========
class ParamInfo:
    def __init__(self, data: dict):
        self.default = data.get("default")
        self.enum = data.get("enum")
        self.name = data.get("name")
        self.optional = data.get("optional")
        self.properties = data.get("properties")
        self.type = data.get("type")

# ========== TypeInfo ==========
class TypeInfo:
    def __init__(self, data: dict):
        self.items = data["items"] if "items" in data else None
        self.typename = data.get("typename")

# ========== PropertyInfo ==========
class PropertyInfo:
    def __init__(self, data: dict):
        self.enum = data.get("enum")
        self.name = data.get("name")
        self.readonly = data.get("readonly")
        if isinstance(data["type"], list):
            print()
        self.type = TypeInfo(data["type"]) if "type" in data else None

# ========== EventInfo ==========
class EventInfo:
    def __init__(self, data: dict):
        self.bubblesFrom = data.get("bubblesFrom")
        self.definedOn = data.get("definedOn")
        self.name = data.get("name")

# ========== ExceptionInfo ==========
class ExceptionInfo:
    def __init__(self, data: dict):
        pass

# ========== ReturnInfo ==========
class ReturnInfo:
    def __init__(self, data: dict):
        self.returnGeneric = data.get("returnGeneric")
        self.returns = data.get("returns")


# ========== IDBType Enum In JS==========
from enum import Enum

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
