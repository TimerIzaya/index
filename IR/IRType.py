# class Type:
#     def __init__(self, typename: str):
#         self.typename = typename
#
#     def __repr__(self):
#         return f"<Type {self.typename}>"
#
#     def __eq__(self, other):
#         if isinstance(other, Type):
#             return self.typename == other.typename
#         return False
#
#     def __hash__(self):
#         return hash(self.typename)
#
#
# # === 基础类型 ===
# string      = Type("string")
# number      = Type("number")\
# boolean     = Type("boolean")
# any         = Type("any")
# null        = Type("null")
# array       = Type("array")
# object      = Type("object")
# function    = Type("function")
# void        = Type("void")
# Promise     = Type("Promise")
#
# # === DOM/Exception/系统类型 ===
# DOMException  = Type("DOMException")
# TypeError     = Type("TypeError")
# DOMStringList = Type("DOMStringList")
#
# # === IndexedDB 类型（对象/接口） ===
# IDBFactory       = Type("IDBFactory")
# IDBDatabase      = Type("IDBDatabase")
# IDBTransaction   = Type("IDBTransaction")
# IDBObjectStore   = Type("IDBObjectStore")
# IDBRequest       = Type("IDBRequest")
# IDBOpenDBRequest = Type("IDBOpenDBRequest")
# IDBIndex         = Type("IDBIndex")
# IDBKeyRange      = Type("IDBKeyRange")
# IDBCursor        = Type("IDBCursor")
# IDBDatabaseInfo  = Type("IDBDatabaseInfo")
#
# # === 泛型返回值中出现的特殊类型 ===
# IDBDatabaseInfo_array = Type("IDBDatabaseInfo[]")
# string_array          = Type("string[]")
#
# # === 全局类型表 ===
# AllIRTypes = {
#     "string": string,
#     "number": number,
#     "boolean": boolean,
#     "any": any,
#     "null": null,
#     "array": array,
#     "object": object,
#     "function": function,
#     "void": void,
#     "Promise": Promise,
#
#     "DOMException": DOMException,
#     "TypeError": TypeError,
#     "DOMStringList": DOMStringList,
#
#     "IDBFactory": IDBFactory,
#     "IDBDatabase": IDBDatabase,
#     "IDBTransaction": IDBTransaction,
#     "IDBObjectStore": IDBObjectStore,
#     "IDBRequest": IDBRequest,
#     "IDBOpenDBRequest": IDBOpenDBRequest,
#     "IDBIndex": IDBIndex,
#     "IDBKeyRange": IDBKeyRange,
#     "IDBCursor": IDBCursor,
#     "IDBDatabaseInfo": IDBDatabaseInfo,
#     "IDBDatabaseInfo[]": IDBDatabaseInfo_array,
#     "string[]": string_array,
# }
