import json
import os

import config
from IR.IRNodes import Program
from IR.IRSchemaParser import IndexedDBSchemaParser
from IR.IRContext import IRContext

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




