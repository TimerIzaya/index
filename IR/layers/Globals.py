# 完整的IR构建过程中所需要的全局变量
from IR.IRContext import IRContext
from IR.layers.IDBContext import IDBContext


class Global:
    irctx = IRContext()
    idbctx = IDBContext()

    @staticmethod
    def reset():
        """重置所有全局上下文"""
        Global.irctx = IRContext()
        Global.idbctx = IDBContext()
