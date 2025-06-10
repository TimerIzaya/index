import json

from IR.IRContext import IRContext
from IR.IRNodes import Identifier
from IR.layers.LiteralContext import LiteralContext
from IR.layers.db_transaction.db_curd.PipeFlow import PipeFlow
from IR.layers.db_transaction.db_curd.PipeGraph import PipeGraph

if __name__ == '__main__':
    irctx = IRContext()
    idbctx = LiteralContext()
    graph = PipeGraph()
    pipes = graph.generate_weighted_path(32, transaction_mode="readwrite")
    flow = PipeFlow(store_id=Identifier("storexxx"), key=1, pipe_ends=pipes)
    il_list = flow.generate_il_sequence()
    for i in il_list:
        print(json.dumps(i.to_dict(), indent=2))
        print("------------")

