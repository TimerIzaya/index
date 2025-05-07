from typing import List

from IR.IRNodes import Identifier
from layers.db_transaction.db_curd.PipeEnd import PipeEnd


class PipeFlow:
    def __init__(self, store_id: Identifier, key, pipe_ends: List[PipeEnd]):
        self.store_id = store_id
        self.key = key
        self.pipe_ends = pipe_ends
        self.il_sequence = []


    def generate_il_sequence(self, irctx, idbctx):
        self.il_sequence = [
            pe.generate_il(self.store_id, self.key, irctx, idbctx)
            for pe in self.pipe_ends
        ]
        return self.il_sequence


    def __len__(self):
        return len(self.pipe_ends)


    def __repr__(self):
        return f"<PipeFlow len={len(self)} key={self.key}>"
