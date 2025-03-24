class Type:
    def __init__(self, name):
        self.typename = name

    def __repr__(self):
        return f"Type({self.typename})"

# === Global Type Constants (auto-generated from schema) ===
DOMException      = Type("DOMException")
string            = Type("string")
number            = Type("number")
any               = Type("any")
TypeError         = Type("TypeError")
array             = Type("array")
object            = Type("object")
boolean           = Type("boolean")
DOMStringList     = Type("DOMStringList")
IDBDatabase       = Type("IDBDatabase")
IDBKeyRange       = Type("IDBKeyRange")
IDBTransaction    = Type("IDBTransaction")
IDBObjectStore    = Type("IDBObjectStore")
IDBRequest        = Type("IDBRequest")
IDBIndex          = Type("IDBIndex")
null              = Type("null")
function          = Type("function")
IDBCursor         = Type("IDBCursor")
