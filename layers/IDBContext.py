import random
from typing import Dict, List, Optional

class IDBContext:
    def __init__(self):
        self.current_db: Optional[str] = None
        self.current_store: Optional[str] = None
        self.database_map: Dict[str, Dict[str, List[str]]] = {}

    def start_database(self, db_name: str):
        self.current_db = db_name
        self.current_store = None
        if db_name not in self.database_map:
            self.database_map[db_name] = {}

    def get_database_name(self) -> str:
        if not self.current_db:
            raise RuntimeError("No active database")
        return self.current_db

    def new_object_store_name(self) -> str:
        """生成一个唯一的 object store 名称，并不注册，仅返回"""
        if self.current_db is None:
            raise RuntimeError("No active database context")

        i = 0
        while True:
            name = f"store_{i}"
            if name not in self.database_map[self.current_db]:
                return name
            i += 1

    def register_object_store(self, store_name: str):
        if self.current_db is None:
            raise RuntimeError("No active database context")
        if store_name not in self.database_map[self.current_db]:
            self.database_map[self.current_db][store_name] = []
        self.current_store = store_name  # ✅ 设置当前 store 上下文

    def new_index_name(self) -> str:
        """为当前 object store 生成一个唯一的 index 名称"""
        if self.current_db is None or self.current_store is None:
            raise RuntimeError("No active database or object store context")

        i = 0
        existing = self.database_map[self.current_db][self.current_store]
        while True:
            name = f"index_{i}"
            if name not in existing:
                return name
            i += 1

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

    def pick_random_object_store(self) -> str:
        stores = self.get_object_stores()
        if not stores:
            raise RuntimeError("No object stores available in current database context")
        return random.choice(stores)
