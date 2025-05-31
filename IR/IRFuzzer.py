from IR.IRContext import IRContext
from layers.IDBContext import IDBContext
from layers.IDBRootLayer import IDBRootLayer

def generate_ir_program():
    irctx = IRContext()
    idbctx = IDBContext()
    root_layer = IDBRootLayer.build(irctx, idbctx)
    return root_layer
