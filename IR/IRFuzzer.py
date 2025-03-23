import config
from IR.IRSchemaParser import IndexedDBSchemaParser
from layers.IDBFactory_OpenDatabase_Layer import build_IDBFactory_OpenDatabase_Layer
from IR.IRContext import IRContext
from layers.IDBOpenDBRequest_onsuccess_Layer import build_IDBOpenDBRequest_onsuccess_Layer
from layers.Layer import Program


def loadFuzzerNeed():
    parser = IndexedDBSchemaParser()
    parser.load()

def generate_simple_ir_program():
    ctx = IRContext()

    layers = [
        build_IDBFactory_OpenDatabase_Layer(ctx),
        build_IDBOpenDBRequest_onsuccess_Layer(ctx)
    ]

    return Program(layers=layers)


if __name__ == "__main__":
    loadFuzzerNeed()
    program = generate_simple_ir_program()
    # print(json.dumps(program.to_dict(), indent=2))
    x = config.GlobalIRTypeRegistry.get_all()
    print(1)
