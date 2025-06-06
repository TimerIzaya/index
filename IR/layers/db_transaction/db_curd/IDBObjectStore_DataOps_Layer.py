from IR.IRContext import IRContext
from IR.IRNodes import CallExpression, Identifier
from IR.IRType import IDBObjectStore
from IR.layers.Globals import Global
from IR.layers.IDBContext import IDBContext
from IR.layers.Layer import Layer, LayerType
from IR.layers.LayerBuilder import LayerBuilder
from IR.layers.db_transaction.db_curd.PipeFlow import PipeFlow
from IR.layers.db_transaction.db_curd.PipeGraph import PipeGraph


class IDBObjectStore_DataOps_Layer(LayerBuilder):
    name = "IDBObjectStore_DataOps_Layer"
    layer_type = LayerType.EXECUTION

    # 可配置项：pipeflow 个数 和 每个长度
    pipeflow_count = 2
    pipeflow_length = 4

    @staticmethod
    def build() -> Layer | None:
        body = []

        store_id: Identifier = Global.irctx.get_identifier_by_type(IDBObjectStore)
        current_store = Global.idbctx.get_current_store()

        # 如果缺少 store 或 name，跳过该层
        if store_id is None or current_store is None:
            return None

        # PipeGraph 用于生成 pipeflow
        graph = PipeGraph()

        for flow_id in range(IDBObjectStore_DataOps_Layer.pipeflow_count):
            key = flow_id + 1  # 每个 flow 对应一个不同的 key
            pipe_ends = graph.generate_weighted_path(
                max_length=IDBObjectStore_DataOps_Layer.pipeflow_length,
                transaction_mode="readwrite"
            )

            pipeflow = PipeFlow(store_id=store_id, key=key, pipe_ends=pipe_ends)
            flow_il = pipeflow.generate_il_sequence()
            body.extend(flow_il)

        return Layer(IDBObjectStore_DataOps_Layer.name, body, layer_type=IDBObjectStore_DataOps_Layer.layer_type)
