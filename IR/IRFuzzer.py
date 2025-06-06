from IR.layers.Globals import Global
from IR.layers.IDBRootLayer import IDBRootLayer

def generate_ir_program():
    Global.reset()
    root_layer = IDBRootLayer.build()
    return root_layer
