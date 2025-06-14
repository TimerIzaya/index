import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# IndexedDB schema 文件路径
SCHEMA_FILE = os.path.join(BASE_DIR, "schema", "indexeddb_schema.json")

FATHER = "window.indexedDB"

IDBFactory_OpenDatabase_Layer = "IDBFactory_OpenDatabase_Layer"
IDBOpenDBRequest_onsuccess_Layer = "IDBOpenDBRequest_onsuccess_Layer"
IDBTransaction_ObjectStoreAccess_Layer = "IDBTransaction_ObjectStoreAccess_Layer"
IDBObjectStore_DataOps_Layer = "IDBObjectStore_DataOps_Layer"

OPTIONAL_JUMP = "__JUMP__"

randomFuzzing = False

class Consts:
    TypeName = "typename"
