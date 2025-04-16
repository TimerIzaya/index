from IR.IRNodes import MemberExpression, CallExpression, Literal, VariableDeclaration, AssignmentExpression, Identifier
from IR.IRContext import IRContext, Variable
from layers.IDBContext import IDBContext
from IR.IRType import IDBObjectStore, IDBIndex, IDBDatabase
import random


def get_store_name(irctx: IRContext, idbctx: IDBContext):
    store = irctx.get_identifier_by_type(IDBObjectStore)
    if store is None:
        raise RuntimeError("No IDBObjectStore identifier available for get_store_name")
    return MemberExpression(store, "name")


def get_store_keypath(irctx: IRContext, idbctx: IDBContext):
    store = irctx.get_identifier_by_type(IDBObjectStore)
    if store is None:
        raise RuntimeError("No IDBObjectStore identifier available for get_store_keypath")
    return MemberExpression(store, "keyPath")


def get_store_autoincrement(irctx: IRContext, idbctx: IDBContext):
    store = irctx.get_identifier_by_type(IDBObjectStore)
    if store is None:
        raise RuntimeError("No IDBObjectStore identifier available for get_store_autoincrement")
    return MemberExpression(store, "autoIncrement")


def get_store_index_names(irctx: IRContext, idbctx: IDBContext):
    store = irctx.get_identifier_by_type(IDBObjectStore)
    if store is None:
        raise RuntimeError("No IDBObjectStore identifier available for get_store_index_names")
    return MemberExpression(store, "indexNames")


def get_index_name(irctx: IRContext, idbctx: IDBContext):
    idx = irctx.get_identifier_by_type(IDBIndex)
    if idx is None:
        raise RuntimeError("No IDBIndex identifier available for get_index_name")
    return MemberExpression(idx, "name")


def get_index_keypath(irctx: IRContext, idbctx: IDBContext):
    idx = irctx.get_identifier_by_type(IDBIndex)
    if idx is None:
        raise RuntimeError("No IDBIndex identifier available for get_index_keypath")
    return MemberExpression(idx, "keyPath")


def get_index_unique(irctx: IRContext, idbctx: IDBContext):
    idx = irctx.get_identifier_by_type(IDBIndex)
    if idx is None:
        raise RuntimeError("No IDBIndex identifier available for get_index_unique")
    return MemberExpression(idx, "unique")


def get_index_multiEntry(irctx: IRContext, idbctx: IDBContext):
    idx = irctx.get_identifier_by_type(IDBIndex)
    if idx is None:
        raise RuntimeError("No IDBIndex identifier available for get_index_multiEntry")
    return MemberExpression(idx, "multiEntry")


def create_object_store(irctx: IRContext, idbctx: IDBContext):
    db = irctx.get_identifier_by_type(IDBDatabase)
    if db is None:
        raise RuntimeError("No IDBDatabase identifier available for create_object_store")
    name = idbctx.new_object_store_name()
    idbctx.register_object_store(name)

    ident = Identifier(name)
    irctx.register_variable(Variable(name, IDBObjectStore))

    return [
        VariableDeclaration(ident.name),
        AssignmentExpression(ident, CallExpression(db, "createObjectStore", [Literal(name)]))
    ]


def delete_object_store(irctx: IRContext, idbctx: IDBContext):
    db = irctx.get_identifier_by_type(IDBDatabase)
    if db is None:
        raise RuntimeError("No IDBDatabase identifier available for delete_object_store")
    name = idbctx.pick_random_object_store()
    if name is None:
        raise RuntimeError("No object store available to delete.")
    return CallExpression(db, "deleteObjectStore", [Literal(name)])


def create_index(irctx: IRContext, idbctx: IDBContext):
    store = irctx.get_identifier_by_type(IDBObjectStore)
    if store is None:
        raise RuntimeError("No IDBObjectStore identifier available for create_index")
    store_name = idbctx.pick_random_object_store()
    if store_name is None:
        raise RuntimeError("No object store available to create index on.")
    index_name = idbctx.new_index_name()
    key_path = Literal(index_name + "_prop")
    idbctx.register_index(store_name, index_name)

    ident = Identifier(index_name)
    irctx.register_variable(Variable(index_name, IDBIndex))

    return [
        VariableDeclaration(ident.name),
        AssignmentExpression(ident, CallExpression(store, "createIndex", [Literal(index_name), key_path]))
    ]


def delete_index(irctx: IRContext, idbctx: IDBContext):
    store = irctx.get_identifier_by_type(IDBObjectStore)
    if store is None:
        raise RuntimeError("No IDBObjectStore identifier available for delete_index")
    idx = idbctx.pick_random_index()
    if idx is None:
        raise RuntimeError("No index available to delete.")
    return CallExpression(store, "deleteIndex", [Literal(idx)])


ReadSchemaOps = [
    get_store_name,
    get_store_keypath,
    get_store_autoincrement,
    get_store_index_names,
    get_index_name,
    get_index_keypath,
    get_index_unique,
    get_index_multiEntry,
]

WriteSchemaOps = [
    create_object_store,
    delete_object_store,
    create_index,
    delete_index,
]

AtomicSchemaOps = ReadSchemaOps + WriteSchemaOps
