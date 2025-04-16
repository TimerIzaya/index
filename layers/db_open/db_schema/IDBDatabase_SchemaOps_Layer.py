from IR.IRContext import IRContext, Variable
from IR.IRNodes import *
from IR.IRType import IDBDatabase, IDBObjectStore
from layers.IDBContext import IDBContext
from layers.Layer import LayerType, Layer
from layers.LayerBuilder import LayerBuilder
from layers.db_open.db_schema.db_schema_opt.AtomicSchemaOps import AtomicSchemaOps, WriteSchemaOps, ReadSchemaOps
import random


class IDBDatabase_SchemaOps_Layer(LayerBuilder):
    name = "IDBDatabase_SchemaOps_Layer"
    layer_type = LayerType.EXECUTION

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        db_ident = irctx.get_identifier_by_type(IDBDatabase)
        body = []

        # 注册一个初始 store（防止 index 创建失败）
        store_name = idbctx.new_object_store_name()
        irctx.register_variable(Variable("store", IDBObjectStore))
        idbctx.register_object_store(store_name)

        # store = db.createObjectStore("store_xxx")
        body.append(
            AssignmentExpression(
                Identifier("store"),
                CallExpression(db_ident, "createObjectStore", [Literal(store_name)])
            )
        )

        # 可配置的读写比
        N = 20
        write_ratio = 0.8
        ops_pool = WriteSchemaOps + ReadSchemaOps
        weights = [write_ratio] * len(WriteSchemaOps) + [(1 - write_ratio)] * len(ReadSchemaOps)

        for _ in range(N):
            op = random.choices(ops_pool, weights=weights, k=1)[0]
            try:
                result = op(irctx, idbctx)
                if isinstance(result, list):
                    body.extend(result)
                elif isinstance(result, IRNode):
                    body.append(result)
                print(f"[AtomicOps] use {op.__name__}: {result}")
            except RuntimeError as e:
                print(f"[AtomicOps] skipped {op.__name__}: {e}")

        return Layer(
            IDBDatabase_SchemaOps_Layer.name,
            body,
            layer_type=IDBDatabase_SchemaOps_Layer.layer_type
        )
