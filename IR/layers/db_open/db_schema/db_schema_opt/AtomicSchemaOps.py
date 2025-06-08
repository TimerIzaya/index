from IR.layers.Globals import Global
from schema.IDBSchemaParser import IDBSchemaParser
from IR.IRNodes import MemberExpression, CallExpression, Literal, VariableDeclaration, AssignmentExpression, Identifier
from IR.IRContext import IRContext, Variable
from IR.IRParamValueGenerator import IRParamValueGenerator
from IR.layers.IDBContext import IDBContext
from IR.IRType import IDBObjectStore, IDBIndex, IDBDatabase


def get_store_name():
    store = Global.irctx.get_identifier_by_type(IDBObjectStore)
    if store is None:
        raise RuntimeError("No IDBObjectStore identifier available for get_store_name")
    return MemberExpression(store, "name")


def get_store_keypath():
    store = Global.irctx.get_identifier_by_type(IDBObjectStore)
    if store is None:
        raise RuntimeError("No IDBObjectStore identifier available for get_store_keypath")
    return MemberExpression(store, "keyPath")


def get_store_autoincrement():
    store = Global.irctx.get_identifier_by_type(IDBObjectStore)
    if store is None:
        raise RuntimeError("No IDBObjectStore identifier available for get_store_autoincrement")
    return MemberExpression(store, "autoIncrement")


def get_store_index_names():
    store = Global.irctx.get_identifier_by_type(IDBObjectStore)
    if store is None:
        raise RuntimeError("No IDBObjectStore identifier available for get_store_index_names")
    return MemberExpression(store, "indexNames")


def get_index_name():
    idx = Global.irctx.get_identifier_by_type(IDBIndex)
    if idx is None:
        raise RuntimeError("No IDBIndex identifier available for get_index_name")
    return MemberExpression(idx, "name")


def get_index_keypath():
    idx = Global.irctx.get_identifier_by_type(IDBIndex)
    if idx is None:
        raise RuntimeError("No IDBIndex identifier available for get_index_keypath")
    return MemberExpression(idx, "keyPath")


def get_index_unique():
    idx = Global.irctx.get_identifier_by_type(IDBIndex)
    if idx is None:
        raise RuntimeError("No IDBIndex identifier available for get_index_unique")
    return MemberExpression(idx, "unique")


def get_index_multiEntry():
    idx = Global.irctx.get_identifier_by_type(IDBIndex)
    if idx is None:
        raise RuntimeError("No IDBIndex identifier available for get_index_multiEntry")
    return MemberExpression(idx, "multiEntry")


def create_object_store():
    db = Global.irctx.get_identifier_by_type(IDBDatabase)
    if db is None:
        raise RuntimeError("No IDBDatabase identifier available for create_object_store")
    name = Global.idbctx.new_object_store_name()
    Global.idbctx.register_object_store(name)
    Global.irctx.register_variable(Variable(name, IDBObjectStore))
    ident = Identifier(name)
    return [
        VariableDeclaration(ident.name),
        AssignmentExpression(ident, CallExpression(db, "createObjectStore", [Literal(name)]))
    ]


def delete_object_store():
    db = Global.irctx.get_identifier_by_type(IDBDatabase)
    if db is None:
        raise RuntimeError("No IDBDatabase identifier available for delete_object_store")
    name = Global.idbctx.pick_random_object_store()
    if name is None:
        raise RuntimeError("No object store available to delete.")
    Global.idbctx.unregister_object_store(name)
    return CallExpression(db, "deleteObjectStore", [Literal(name)])


def create_index():
    parser = IDBSchemaParser()
    method = parser.getInterface("IDBObjectStore").getInstanceMethod("createIndex")

    # 首先确保当前上下文中有有效的 object store
    store = Global.irctx.get_identifier_by_type(IDBObjectStore)
    if store is None:
        raise RuntimeError("No IDBObjectStore available")

    # 尝试生成一个唯一的 index 名称，避免与已有 index 冲突
    store_name = Global.idbctx.get_current_store()
    if not store_name:
        raise RuntimeError("No current store in context")

    # 尝试最多 5 次获取一个不重复的 index 名称
    for _ in range(5):
        index_name = Global.idbctx.new_index_name()
        if not Global.idbctx.has_index(store_name, index_name):
            break
    else:
        raise RuntimeError(f"Unable to generate unique index name for store: {store_name}")

    # 注册该索引名称
    Global.idbctx.register_index(store_name, index_name)

    # 生成参数列表
    args = IRParamValueGenerator.generateMethodArgs(method.node)

    ident = Identifier(index_name)
    Global.irctx.register_variable(Variable(index_name, IDBIndex))

    return [
        VariableDeclaration(ident.name),
        AssignmentExpression(
            ident,
            CallExpression(store, "createIndex", args)
        )
    ]


def delete_index():
    store = Global.irctx.get_identifier_by_type(IDBObjectStore)
    if store is None:
        raise RuntimeError("No IDBObjectStore identifier available for delete_index")

    idx = Global.idbctx.pick_random_index()
    if idx is None:
        raise RuntimeError("No index available to delete.")
    store_name = Global.idbctx.current_store

    Global.idbctx.unregister_index(store_name, idx)
    return CallExpression(store, "deleteIndex", [Literal(idx)])


# 每个操作函数的独立权重配置
AtomicSchemaWeights = {
    get_store_name: 1,
    get_store_keypath: 1,
    get_store_autoincrement: 1,
    get_store_index_names: 1,
    get_index_name: 1,
    get_index_keypath: 1,
    get_index_unique: 1,
    get_index_multiEntry: 1,
    create_object_store: 5,
    delete_object_store: 5,
    create_index: 10,
    delete_index: 2,
}

# 自动构造列表
ReadSchemaOps = [f for f in [
    get_store_name,
    get_store_keypath,
    get_store_autoincrement,
    get_store_index_names,
    get_index_name,
    get_index_keypath,
    get_index_unique,
    get_index_multiEntry
] if AtomicSchemaWeights.get(f, 0) > 0]

WriteSchemaOps = [f for f in [
    create_object_store,
    delete_object_store,
    create_index,
    delete_index
] if AtomicSchemaWeights.get(f, 0) > 0]

AtomicSchemaOps = ReadSchemaOps + WriteSchemaOps
