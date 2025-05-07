from layers.db_transaction.db_curd.PipeEnd import PipeEnd


# === STEP 2: 定义 Pipe ===
class Pipe:
    def __init__(self, src: PipeEnd, dst: PipeEnd, key_aware: bool, weight: float):
        self.src = src
        self.dst = dst
        self.key_aware = key_aware
        self.weight = weight

    def __repr__(self):
        return f"Pipe({self.src.name} -> {self.dst.name}, {'key-aware' if self.key_aware else 'non-aware'}, weight={self.weight})"
