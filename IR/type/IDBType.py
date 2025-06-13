# ========== IDBType Enum ==========
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
    IDBFactory = "IDBFactory"

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
