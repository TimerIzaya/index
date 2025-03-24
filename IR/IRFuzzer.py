import json

import config
from IR.IRSchemaParser import IndexedDBSchemaParser
from IR.IRContext import IRContext
from layers.IDBFactory_OpenDatabase_Layer import IDBFactory_OpenDatabase_Layer
from layers.IDBRootLayer import IDBRootLayer
from layers.Layer import Program


def loadFuzzerNeed():
    parser = IndexedDBSchemaParser()
    parser.load()

def generate_simple_ir_program():
    ctx = IRContext()

    layers = [
        IDBRootLayer.build(ctx),  # ✅ 全局初始化
        IDBFactory_OpenDatabase_Layer.build(ctx),
    ]
    return Program(layers=layers)


if __name__ == "__main__":
    loadFuzzerNeed()
    program = generate_simple_ir_program()
    print(json.dumps(program.to_dict(), indent=2))
