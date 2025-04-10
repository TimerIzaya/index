from IR.IRContext import IRContext, Variable
from IR.IRType import IDBFactory, IDBDatabase
from IR.IRNodes import VariableDeclaration
from layers.IDBContext import IDBContext
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.IDBFactory_OpenDatabase_Layer import IDBFactory_OpenDatabase_Layer
from layers.db_delete.IDBFactory_DeleteDatabase_Layer import IDBFactory_DeleteDatabase_Layer


class IDBRootLayer(LayerBuilder):
    name = "IDBRootLayer"
    layer_type = LayerType.CALLING

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        # 注册 indexedDB 对象
        irctx.register_variable(Variable("window.indexedDB", IDBFactory))

        # 全局声明 db 变量
        irctx.register_variable(Variable("db", IDBDatabase))
        db_decl = VariableDeclaration(name="db", kind="let")

        # 构建子层：open / delete
        open_layer = IDBFactory_OpenDatabase_Layer.build(irctx, idbctx)
        delete_layer = IDBFactory_DeleteDatabase_Layer.build(irctx, idbctx)

        return Layer(
            name=IDBRootLayer.name,
            ir_nodes=[db_decl],
            children=[open_layer, delete_layer],
            layer_type=IDBRootLayer.layer_type
        )
