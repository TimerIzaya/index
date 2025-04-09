import random
from typing import Dict, List, Optional

class IDBContext:
    def __init__(self):
        self.current_db: Optional[str] = None
        self.database_map: Dict[str, Dict[str, List[str]]] = {}

    def start_database(self, db_name: str):
        self.current_db = db_name
        if db_name not in self.database_map:
            self.database_map[db_name] = {}

    def register_object_store(self, store_name: str):
        if self.current_db is None:
            raise RuntimeError("No active database context")
        if store_name not in self.database_map[self.current_db]:
            self.database_map[self.current_db][store_name] = []

    def register_index(self, store_name: str, index_name: str):
        if self.current_db is None:
            raise RuntimeError("No active database context")
        if store_name not in self.database_map[self.current_db]:
            self.register_object_store(store_name)
        self.database_map[self.current_db][store_name].append(index_name)

    def get_object_stores(self) -> List[str]:
        if self.current_db and self.current_db in self.database_map:
            return list(self.database_map[self.current_db].keys())
        return []

    def get_indexes(self, store_name: str) -> List[str]:
        if self.current_db and store_name in self.database_map.get(self.current_db, {}):
            return self.database_map[self.current_db][store_name]
        return []

    # ✅ 新增方法：随机获取一个 object store 名称
    def pick_random_object_store(self) -> str:
        stores = self.get_object_stores()
        if not stores:
            raise RuntimeError("No object stores available in current database context")
        return random.choice(stores)
