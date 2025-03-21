from typing import List, Optional, Dict

# ========== InterfaceInfo ==========
class InterfaceInfo:
    def __init__(self, data: dict):
        self.category = data.get("category")
        self.events = data.get("events")
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
        self.items = data.get("items")
        self.typename = data.get("typename")

# ========== PropertyInfo ==========
class PropertyInfo:
    def __init__(self, data: dict):
        self.enum = data.get("enum")
        self.name = data.get("name")
        self.readonly = data.get("readonly")
        self.type = data.get("type")

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
