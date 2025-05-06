from schema.SchemaClass import MethodInfo
from schema.SchemaInstanceTree import initialize_interfaces, ALL_INTERFACES
from typing import List
import random

class PipeEnd:
    def __init__(self, method_info: MethodInfo):
        self.name = method_info.name
        self.method_info = method_info
        self.is_read = self._infer_is_read()
        self.is_write = self._infer_is_write()

    def _infer_is_read(self):
        return self.name in {"get", "getAll", "getAllKeys", "getKey", "count", "openCursor", "openKeyCursor"}

    def _infer_is_write(self):
        return self.name in {"put", "add", "delete", "clear"}

    def __repr__(self):
        return f"PipeEnd({self.name})"


# === STEP 2: 定义 Pipe ===
class Pipe:
    def __init__(self, src: PipeEnd, dst: PipeEnd, key_aware: bool, weight: float):
        self.src = src
        self.dst = dst
        self.key_aware = key_aware
        self.weight = weight

    def __repr__(self):
        return f"Pipe({self.src.name} -> {self.dst.name}, {'key-aware' if self.key_aware else 'non-aware'}, weight={self.weight})"

# === STEP 3: PipeGraph 类 ===
class PipeGraph:
    def __init__(self):
        initialize_interfaces()
        self.interface = ALL_INTERFACES["IDBObjectStore"]

        self.pipe_ends: List[PipeEnd] = []
        self.pipes: List[Pipe] = []

        # 初始化所有 PipeEnd
        self.pe_put = self._add_pipe_end("put")
        self.pe_add = self._add_pipe_end("add")
        self.pe_get = self._add_pipe_end("get")
        self.pe_getAll = self._add_pipe_end("getAll")
        self.pe_getAllKeys = self._add_pipe_end("getAllKeys")
        self.pe_getKey = self._add_pipe_end("getKey")
        self.pe_delete = self._add_pipe_end("delete")
        self.pe_clear = self._add_pipe_end("clear")
        self.pe_count = self._add_pipe_end("count")
        self.pe_openCursor = self._add_pipe_end("openCursor")
        self.pe_openKeyCursor = self._add_pipe_end("openKeyCursor")

        # 初始化所有 Pipe（True 为 key-aware，False 为 non-aware）
        # High weight (1.0)
        self._add_pipe(self.pe_put, self.pe_get, True, 1.0)
        self._add_pipe(self.pe_put, self.pe_delete, True, 1.0)
        self._add_pipe(self.pe_add, self.pe_get, True, 1.0)
        self._add_pipe(self.pe_add, self.pe_delete, True, 1.0)
        self._add_pipe(self.pe_get, self.pe_count, True, 1.0)
        self._add_pipe(self.pe_delete, self.pe_count, True, 1.0)
        self._add_pipe(self.pe_clear, self.pe_put, False, 1.0)
        self._add_pipe(self.pe_clear, self.pe_add, False, 1.0)
        self._add_pipe(self.pe_openCursor, self.pe_put, False, 1.0)
        self._add_pipe(self.pe_openCursor, self.pe_delete, False, 1.0)
        self._add_pipe(self.pe_openKeyCursor, self.pe_put, False, 1.0)
        self._add_pipe(self.pe_openKeyCursor, self.pe_delete, False, 1.0)

        # Medium weight (0.6) - self-loop
        self._add_pipe(self.pe_put, self.pe_put, True, 0.6)
        self._add_pipe(self.pe_add, self.pe_add, True, 0.6)
        self._add_pipe(self.pe_get, self.pe_get, True, 0.6)
        self._add_pipe(self.pe_getAll, self.pe_getAll, False, 0.6)
        self._add_pipe(self.pe_getAllKeys, self.pe_getAllKeys, False, 0.6)
        self._add_pipe(self.pe_getKey, self.pe_getKey, True, 0.6)
        self._add_pipe(self.pe_delete, self.pe_delete, True, 0.6)
        self._add_pipe(self.pe_clear, self.pe_clear, False, 0.6)
        self._add_pipe(self.pe_count, self.pe_count, False, 0.6)
        self._add_pipe(self.pe_openCursor, self.pe_openCursor, False, 0.6)
        self._add_pipe(self.pe_openKeyCursor, self.pe_openKeyCursor, False, 0.6)

        # Low weight (0.2) - all other combinations not excluded
        self._add_pipe(self.pe_put, self.pe_add, True, 0.2)
        self._add_pipe(self.pe_put, self.pe_getAll, False, 0.2)
        self._add_pipe(self.pe_put, self.pe_getAllKeys, False, 0.2)
        self._add_pipe(self.pe_put, self.pe_getKey, True, 0.2)
        self._add_pipe(self.pe_put, self.pe_clear, False, 0.2)
        self._add_pipe(self.pe_put, self.pe_count, False, 0.2)
        self._add_pipe(self.pe_put, self.pe_openCursor, False, 0.2)
        self._add_pipe(self.pe_put, self.pe_openKeyCursor, False, 0.2)

        self._add_pipe(self.pe_add, self.pe_put, True, 0.2)
        self._add_pipe(self.pe_add, self.pe_getAll, False, 0.2)
        self._add_pipe(self.pe_add, self.pe_getAllKeys, False, 0.2)
        self._add_pipe(self.pe_add, self.pe_getKey, True, 0.2)
        self._add_pipe(self.pe_add, self.pe_clear, False, 0.2)
        self._add_pipe(self.pe_add, self.pe_count, False, 0.2)
        self._add_pipe(self.pe_add, self.pe_openCursor, False, 0.2)
        self._add_pipe(self.pe_add, self.pe_openKeyCursor, False, 0.2)

        self._add_pipe(self.pe_get, self.pe_put, True, 0.2)
        self._add_pipe(self.pe_get, self.pe_add, True, 0.2)
        self._add_pipe(self.pe_get, self.pe_getAll, False, 0.2)
        self._add_pipe(self.pe_get, self.pe_getAllKeys, False, 0.2)
        self._add_pipe(self.pe_get, self.pe_getKey, True, 0.2)
        self._add_pipe(self.pe_get, self.pe_clear, False, 0.2)
        self._add_pipe(self.pe_get, self.pe_delete, True, 0.2)
        self._add_pipe(self.pe_get, self.pe_openCursor, False, 0.2)
        self._add_pipe(self.pe_get, self.pe_openKeyCursor, False, 0.2)

        self._add_pipe(self.pe_getAll, self.pe_put, False, 0.2)
        self._add_pipe(self.pe_getAll, self.pe_add, False, 0.2)
        self._add_pipe(self.pe_getAll, self.pe_delete, False, 0.2)
        self._add_pipe(self.pe_getAll, self.pe_clear, False, 0.2)
        self._add_pipe(self.pe_getAll, self.pe_count, False, 0.2)
        self._add_pipe(self.pe_getAll, self.pe_openCursor, False, 0.2)
        self._add_pipe(self.pe_getAll, self.pe_openKeyCursor, False, 0.2)

        self._add_pipe(self.pe_getAllKeys, self.pe_put, False, 0.2)
        self._add_pipe(self.pe_getAllKeys, self.pe_add, False, 0.2)
        self._add_pipe(self.pe_getAllKeys, self.pe_delete, False, 0.2)
        self._add_pipe(self.pe_getAllKeys, self.pe_clear, False, 0.2)
        self._add_pipe(self.pe_getAllKeys, self.pe_count, False, 0.2)
        self._add_pipe(self.pe_getAllKeys, self.pe_openCursor, False, 0.2)
        self._add_pipe(self.pe_getAllKeys, self.pe_openKeyCursor, False, 0.2)

        self._add_pipe(self.pe_getKey, self.pe_put, True, 0.2)
        self._add_pipe(self.pe_getKey, self.pe_add, True, 0.2)
        self._add_pipe(self.pe_getKey, self.pe_getAll, False, 0.2)
        self._add_pipe(self.pe_getKey, self.pe_getAllKeys, False, 0.2)
        self._add_pipe(self.pe_getKey, self.pe_clear, False, 0.2)
        self._add_pipe(self.pe_getKey, self.pe_delete, True, 0.2)
        self._add_pipe(self.pe_getKey, self.pe_count, False, 0.2)
        self._add_pipe(self.pe_getKey, self.pe_openCursor, False, 0.2)
        self._add_pipe(self.pe_getKey, self.pe_openKeyCursor, False, 0.2)

        self._add_pipe(self.pe_delete, self.pe_put, True, 0.2)
        self._add_pipe(self.pe_delete, self.pe_add, True, 0.2)
        self._add_pipe(self.pe_delete, self.pe_getAll, False, 0.2)
        self._add_pipe(self.pe_delete, self.pe_getAllKeys, False, 0.2)
        self._add_pipe(self.pe_delete, self.pe_getKey, True, 0.2)
        self._add_pipe(self.pe_delete, self.pe_clear, False, 0.2)
        self._add_pipe(self.pe_delete, self.pe_openCursor, False, 0.2)
        self._add_pipe(self.pe_delete, self.pe_openKeyCursor, False, 0.2)

        self._add_pipe(self.pe_clear, self.pe_get, False, 0.2)
        self._add_pipe(self.pe_clear, self.pe_getAll, False, 0.2)
        self._add_pipe(self.pe_clear, self.pe_getAllKeys, False, 0.2)
        self._add_pipe(self.pe_clear, self.pe_getKey, False, 0.2)
        self._add_pipe(self.pe_clear, self.pe_count, False, 0.2)
        self._add_pipe(self.pe_clear, self.pe_openCursor, False, 0.2)
        self._add_pipe(self.pe_clear, self.pe_openKeyCursor, False, 0.2)

        self._add_pipe(self.pe_count, self.pe_put, False, 0.2)
        self._add_pipe(self.pe_count, self.pe_add, False, 0.2)
        self._add_pipe(self.pe_count, self.pe_getAll, False, 0.2)
        self._add_pipe(self.pe_count, self.pe_getAllKeys, False, 0.2)
        self._add_pipe(self.pe_count, self.pe_getKey, False, 0.2)
        self._add_pipe(self.pe_count, self.pe_delete, False, 0.2)
        self._add_pipe(self.pe_count, self.pe_clear, False, 0.2)
        self._add_pipe(self.pe_count, self.pe_openCursor, False, 0.2)
        self._add_pipe(self.pe_count, self.pe_openKeyCursor, False, 0.2)

        self._add_pipe(self.pe_openCursor, self.pe_get, False, 0.2)
        self._add_pipe(self.pe_openCursor, self.pe_getAll, False, 0.2)
        self._add_pipe(self.pe_openCursor, self.pe_getAllKeys, False, 0.2)
        self._add_pipe(self.pe_openCursor, self.pe_getKey, False, 0.2)
        self._add_pipe(self.pe_openCursor, self.pe_clear, False, 0.2)
        self._add_pipe(self.pe_openCursor, self.pe_count, False, 0.2)
        self._add_pipe(self.pe_openCursor, self.pe_openKeyCursor, False, 0.2)

        self._add_pipe(self.pe_openKeyCursor, self.pe_get, False, 0.2)
        self._add_pipe(self.pe_openKeyCursor, self.pe_getAll, False, 0.2)
        self._add_pipe(self.pe_openKeyCursor, self.pe_getAllKeys, False, 0.2)
        self._add_pipe(self.pe_openKeyCursor, self.pe_getKey, False, 0.2)
        self._add_pipe(self.pe_openKeyCursor, self.pe_clear, False, 0.2)
        self._add_pipe(self.pe_openKeyCursor, self.pe_count, False, 0.2)
        self._add_pipe(self.pe_openKeyCursor, self.pe_openCursor, False, 0.2)

    def _add_pipe_end(self, name: str) -> PipeEnd:
        method = self.interface.instanceMethods[name]
        pe = PipeEnd(method)
        self.pipe_ends.append(pe)
        return pe

    def _add_pipe(self, src: PipeEnd, dst: PipeEnd, key_aware: bool, weight: float):
        self.pipes.append(Pipe(src, dst, key_aware, weight))

    def generate_weighted_path(self, max_length=6, transaction_mode="readwrite"):
        path = []
        current = random.choice(self.pipe_ends)
        path.append(current)

        for _ in range(max_length - 1):
            candidates = [p for p in self.pipes if p.src == current]

            # 根据事务模式调整权重
            if transaction_mode == "readonly":
                weights = [p.weight * 0.1 if p.dst.is_write else p.weight for p in candidates]
            else:
                weights = [p.weight for p in candidates]

            if not candidates:
                break
            next_pipe = random.choices(candidates, weights=weights)[0]
            current = next_pipe.dst
            path.append(current)

        return path

    def __repr__(self):
        return f"PipeGraph with {len(self.pipe_ends)} ends and {len(self.pipes)} pipes:\n" + "\n".join(repr(p) for p in self.pipes)

if __name__ == "__main__":
    graph = PipeGraph()
    g = graph.generate_weighted_path(16, "readonly")
    for i in g:
        print(i)
