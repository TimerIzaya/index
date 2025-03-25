import json

import config
from IR.IRSchemaParser import IndexedDBSchemaParser
from IR.IRContext import IRContext
from layers.Layer import Program

# 导入所有 Layer
from layers.IDBRootLayer import IDBRootLayer
from layers.IDBFactory_OpenDatabase_Layer import IDBFactory_OpenDatabase_Layer
from layers.IDBOpenDBRequest_onsuccess_Layer import IDBOpenDBRequest_onsuccess_Layer


def loadFuzzerNeed():
    parser = IndexedDBSchemaParser()
    parser.load()


def generate_ir_program():
    ctx = IRContext()
    root_layer = IDBRootLayer.build(ctx)
    return Program(layers=[root_layer])



if __name__ == "__main__":
    loadFuzzerNeed()
    program = generate_ir_program()
    print(json.dumps(program.to_dict(), indent=2))
