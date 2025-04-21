import random
from layers.db_open.db_schema.db_schema_opt.AtomicSchemaOps import (
    AtomicSchemaWeights, ReadSchemaOps, WriteSchemaOps
)
from layers.db_open.db_schema.db_schema_opt.CompoundSchemaOps import (
    CompoundOpWeights
)

class SchemaOptDispatcher:

    def __init__(self):
        self.atomic_ops = [
            f for f in AtomicSchemaWeights if AtomicSchemaWeights[f] > 0
        ]
        self.compound_ops = [
            f for f in CompoundOpWeights if CompoundOpWeights[f] > 0
        ]
        self.all_ops = self.atomic_ops + self.compound_ops

    def get_all_ops(self):
        return self.all_ops

    def get_atomic_ops(self):
        return self.atomic_ops

    def get_compound_ops(self):
        return self.compound_ops

    def get_weight(self, op):
        return AtomicSchemaWeights.get(op, CompoundOpWeights.get(op, 0))

    def choose_op(self):
        ops = self.all_ops
        weights = [self.get_weight(op) for op in ops]
        return random.choices(ops, weights=weights, k=1)[0]
