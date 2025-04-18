# CompoundSchemaOps.py

from layers.db_open.db_schema.db_schema_opt.AtomicSchemaOps import *
import random

# replace 系列（含 recreate 行为）

def replace_index(irctx, idbctx):
    return [
        delete_index(irctx, idbctx),
        *create_index(irctx, idbctx)
    ]

def replace_object_store(irctx, idbctx):
    return [
        delete_object_store(irctx, idbctx),
        *create_object_store(irctx, idbctx)
    ]

def replace_store_name(irctx, idbctx):
    return replace_object_store(irctx, idbctx)

def replace_store_keypath(irctx, idbctx):
    return replace_object_store(irctx, idbctx)

def replace_store_autoincrement(irctx, idbctx):
    return replace_object_store(irctx, idbctx)

def replace_index_name(irctx, idbctx):
    return replace_index(irctx, idbctx)

def replace_index_keypath(irctx, idbctx):
    return replace_index(irctx, idbctx)

def replace_index_unique(irctx, idbctx):
    return replace_index(irctx, idbctx)

def replace_index_multiEntry(irctx, idbctx):
    return replace_index(irctx, idbctx)

# add 系列

def add_multiple_indexes(irctx, idbctx):
    stmts = []
    for _ in range(random.randint(2, 5)):
        stmts.extend(create_index(irctx, idbctx))
    return stmts


# drop 系列

def drop_all_indexes(irctx, idbctx):
    all_indexes = idbctx.get_all_indexes()
    if not all_indexes:
        raise RuntimeError("No indexes to drop")
    stmts = []
    for _ in all_indexes:
        stmts.append(delete_index(irctx, idbctx))
    return stmts

# reset 系列

def reset_schema(irctx, idbctx):
    return [
        delete_object_store(irctx, idbctx),
        delete_object_store(irctx, idbctx),
        *create_object_store(irctx, idbctx),
        *create_index(irctx, idbctx)
    ]

CompoundSchemaOps = {
    "replace": [
        replace_index,
        replace_object_store,
        replace_store_name,
        replace_store_keypath,
        replace_store_autoincrement,
        replace_index_name,
        replace_index_keypath,
        replace_index_unique,
        replace_index_multiEntry
    ],
    "add": [add_multiple_indexes],
    "drop": [drop_all_indexes],
    "reset": [reset_schema],
}

CompoundSchemaWeights = {
    "replace": 5,
    "add": 3,
    "drop": 2,
    "reset": 1,
}

def choose_random_compound_op():
    op_type = random.choices(
        population=list(CompoundSchemaOps.keys()),
        weights=[CompoundSchemaWeights[k] for k in CompoundSchemaOps.keys()],
        k=1
    )[0]
    return random.choice(CompoundSchemaOps[op_type])
