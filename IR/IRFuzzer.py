from IR.IRNodes import IRNode
from IR.IRSchemaParser import IndexedDBSchemaParser
from IR.IRContext import IRContext
from layers.IDBContext import IDBContext

# 导入所有 Layer
from layers.IDBRootLayer import IDBRootLayer
from layers.Layer import Layer



def loadFuzzerNeed():
    parser = IndexedDBSchemaParser()
    parser.load()


def generate_ir_program():
    irctx = IRContext()
    idbctx = IDBContext()
    root_layer = IDBRootLayer.build(irctx, idbctx)
    return root_layer
