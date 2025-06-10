# 完整的IR构建过程中所需要的全局变量
from IR.IRContext import IRContext
from IR.layers.LiteralContext import LiteralContext


class Global:
    irctx = IRContext()
    itctx = LiteralContext()

    @staticmethod
    def reset():
        """重置所有全局上下文"""
        Global.irctx = IRContext()
        Global.itctx = LiteralContext()
