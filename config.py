import os
from IR.IRTypeRegistry import IRTypeRegistry

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# IndexedDB schema 文件路径
SCHEMA_FILE = os.path.join(BASE_DIR, "schema", "indexeddb_schema.json")


GlobalIRTypeRegistry = IRTypeRegistry()

IDBFactory_OpenDatabase_Layer = "IDBFactory_OpenDatabase_Layer"
IDBOpenDBRequest_onsuccess_Layer = "IDBOpenDBRequest_onsuccess_Layer"
IDBTransaction_ObjectStoreAccess_Layer = "IDBTransaction_ObjectStoreAccess_Layer"
IDBObjectStore_DataOps_Layer = "IDBObjectStore_DataOps_Layer"


class Consts:
    TypeName = "typename"
