from IR.IRContext import IRContext
from IR.IRNodes import *
from layers.IDBContext import IDBContext
from layers.Layer import LayerType, Layer
from layers.LayerBuilder import LayerBuilder
from layers.db_open.db_schema.db_schema_opt.AtomicSchemaOps import create_object_store, create_index
from layers.db_open.db_schema.db_schema_opt.SchemaOptDispatcher import SchemaOptDispatcher
import random


class IDBDatabase_SchemaOps_Layer(LayerBuilder):
    name = "IDBDatabase_SchemaOps_Layer"
    layer_type = LayerType.EXECUTION

    # 配置项
    total_ops = 20

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        body = []

        # 初始创建一个 object store 和一个 index
        body.extend(create_object_store(irctx, idbctx))
        body.extend(create_index(irctx, idbctx))

        dispatcher = SchemaOptDispatcher()

        for _ in range(IDBDatabase_SchemaOps_Layer.total_ops):
            op = dispatcher.choose_op()
            try:
                result = op(irctx, idbctx)
                if isinstance(result, list):
                    body.extend(result)
                elif isinstance(result, IRNode):
                    body.append(result)
                print(f"[SchemaOpt] use {op.__name__}")
            except RuntimeError as e:
                print(f"[SchemaOpt] skipped {op.__name__}: {e}")

        return Layer(
            IDBDatabase_SchemaOps_Layer.name,
            body,
            layer_type=IDBDatabase_SchemaOps_Layer.layer_type
        )
