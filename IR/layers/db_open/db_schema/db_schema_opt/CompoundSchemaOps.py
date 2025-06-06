# CompoundSchemaOps.py

from IR.layers.db_open.db_schema.db_schema_opt.AtomicSchemaOps import *
import random


# replace 系列（含 recreate 行为）

def replace_index():
    return [
        delete_index(),
        *create_index()
    ]


def replace_object_store():
    return [
        delete_object_store(),
        *create_object_store()
    ]


def replace_store_name():
    return replace_object_store()


def replace_store_keypath():
    return replace_object_store()


def replace_store_autoincrement():
    return replace_object_store()


def replace_index_name():
    return replace_index()


def replace_index_keypath():
    return replace_index()


def replace_index_unique():
    return replace_index()


def replace_index_multiEntry():
    return replace_index()


# add 系列

def add_multiple_indexes():
    stmts = []
    for _ in range(random.randint(2, 5)):
        stmts.extend(create_index())
    return stmts


# drop 系列

def drop_all_indexes():
    all_indexes = Global.idbctx.get_all_indexes()
    if not all_indexes:
        raise RuntimeError("No indexes to drop")
    stmts = []
    for _ in all_indexes:
        stmts.append(delete_index())
    return stmts


# reset 系列

def reset_schema():
    return [
        delete_object_store(),
        delete_object_store(),
        *create_object_store(),
        *create_index()
    ]


# 每个复合操作函数绑定权重
CompoundOpWeights = {
    replace_index: 3,
    replace_object_store: 3,
    replace_store_name: 2,
    replace_store_keypath: 2,
    replace_store_autoincrement: 2,
    replace_index_name: 2,
    replace_index_keypath: 2,
    replace_index_unique: 2,
    replace_index_multiEntry: 2,
    add_multiple_indexes: 3,
    drop_all_indexes: 1,
    reset_schema: 1,
}

# 平铺所有操作（替代旧的分组方式）
FlatCompoundOps = [
    f for f, w in CompoundOpWeights.items() if w > 0
]

def choose_random_compound_op():
    ops = FlatCompoundOps
    weights = [CompoundOpWeights[f] for f in ops]
    return random.choices(ops, weights=weights, k=1)[0]
