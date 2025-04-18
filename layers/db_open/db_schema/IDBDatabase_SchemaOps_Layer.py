from IR.IRContext import IRContext
from IR.IRNodes import *
from layers.IDBContext import IDBContext
from layers.Layer import LayerType, Layer
from layers.LayerBuilder import LayerBuilder
from layers.db_open.db_schema.db_schema_opt.AtomicSchemaOps import AtomicSchemaOps, WriteSchemaOps, ReadSchemaOps, \
    create_object_store, create_index
from layers.db_open.db_schema.db_schema_opt.CompoundSchemaOps import CompoundSchemaOps, CompoundSchemaWeights
import random


class IDBDatabase_SchemaOps_Layer(LayerBuilder):
    name = "IDBDatabase_SchemaOps_Layer"
    layer_type = LayerType.EXECUTION

    # 配置项（可在外部传参或重载）
    enable_atomic = False
    enable_compound = True
    atomic_ratio = 0.7  # atomic : compound = 7:3
    use_write_only = False  # 若为 True，则 Atomic 中只使用 WriteSchemaOps
    total_ops = 1  # 所有操作总数（原子+复合）

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        body = []
        body.extend(create_object_store(irctx, idbctx))
        body.extend(create_index(irctx, idbctx))

    # # ✅ 初始创建一个 object store 和一个 index，避免后续空上下文
    # try:
    #     body.extend(create_object_store(irctx, idbctx))
    #     body.extend(create_index(irctx, idbctx))
    # except RuntimeError as e:
    #     print(f"[Init] Failed to create store/index: {e}")
    #
    # atomic_ops = WriteSchemaOps if IDBDatabase_SchemaOps_Layer.use_write_only else AtomicSchemaOps
    # compound_types = list(CompoundSchemaOps.keys())
    # compound_weights = [CompoundSchemaWeights[k] for k in compound_types]
    #
    # N = IDBDatabase_SchemaOps_Layer.total_ops
    # for _ in range(N):
    #     use_atomic = False
    #     if IDBDatabase_SchemaOps_Layer.enable_atomic and IDBDatabase_SchemaOps_Layer.enable_compound:
    #         use_atomic = random.random() < IDBDatabase_SchemaOps_Layer.atomic_ratio
    #     elif IDBDatabase_SchemaOps_Layer.enable_atomic:
    #         use_atomic = True
    #
    #     if use_atomic:
    #         op = random.choice(atomic_ops)
    #         tag = "Atomic"
    #     else:
    #         op_type = random.choices(compound_types, weights=compound_weights, k=1)[0]
    #         op = random.choice(CompoundSchemaOps[op_type])
    #         tag = f"Compound[{op_type}]"
    #
    #     try:
    #         result = op(irctx, idbctx)
    #         if isinstance(result, list):
    #             body.extend(result)
    #         elif isinstance(result, IRNode):
    #             body.append(result)
    #         print(f"[{tag}] use {op.__name__}")
    #     except RuntimeError as e:
    #         print(f"[{tag}] skipped {op.__name__}: {e}")

        return Layer(
            IDBDatabase_SchemaOps_Layer.name,
            body,
            layer_type=IDBDatabase_SchemaOps_Layer.layer_type
        )
