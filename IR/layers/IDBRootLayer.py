from IR.IRContext import IRContext, Variable
from IR.IRType import IDBFactory, IDBDatabase
from IR.IRNodes import VariableDeclaration
from IR.layers.Globals import Global
from IR.layers.IDBContext import IDBContext
from IR.layers.Layer import Layer, LayerType
from IR.layers.LayerBuilder import LayerBuilder
from IR.layers.db_open.IDBFactory_OpenDatabase_Layer import IDBFactory_OpenDatabase_Layer
from IR.layers.db_delete.IDBFactory_DeleteDatabase_Layer import IDBFactory_DeleteDatabase_Layer


class IDBRootLayer(LayerBuilder):
    name = "IDBRootLayer"
    layer_type = LayerType.CALLING

    @staticmethod
    def build() -> Layer:
        # 全局声明 db 变量
        Global.irctx.register_variable(Variable("db", IDBDatabase))
        db_decl = VariableDeclaration(name="db", kind="let")

        # 构建子层：open / delete
        open_layer = IDBFactory_OpenDatabase_Layer.build()
        delete_layer = IDBFactory_DeleteDatabase_Layer.build()

        return Layer(
            name=IDBRootLayer.name,
            ir_nodes=[db_decl],
            children=[open_layer, delete_layer],
            layer_type=IDBRootLayer.layer_type
        )
