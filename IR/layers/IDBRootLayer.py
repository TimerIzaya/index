from IR.IRContext import IRContext, Variable
from IR.IRNodes import VariableDeclaration, Identifier
from IR.layers.Globals import Global
from IR.layers.Layer import Layer, LayerType
from IR.layers.LayerBuilder import LayerBuilder
from IR.layers.db_open.IDBFactory_OpenDatabase_Layer import IDBFactory_OpenDatabase_Layer
from IR.layers.db_delete.IDBFactory_DeleteDatabase_Layer import IDBFactory_DeleteDatabase_Layer
from IR.type.IDBType import IDBType


class IDBRootLayer(LayerBuilder):
    name = "IDBRootLayer"
    layer_type = LayerType.CALLING

    @staticmethod
    def build() -> Layer:
        Global.irctx.enter_layer(IDBRootLayer)
        # 全局声明 db 变量
        Global.irctx.register_variable(Variable("db", IDBType.IDBDatabase))
        db_decl = VariableDeclaration(name="db", kind="let")

        # 构建子层：open / delete
        open_layer = IDBFactory_OpenDatabase_Layer.build()
        delete_layer = IDBFactory_DeleteDatabase_Layer.build()


        Global.irctx.exit_layer()
        return Layer(
            name=IDBRootLayer.name,
            ir_nodes=[db_decl],
            children=[open_layer, delete_layer],
            layer_type=IDBRootLayer.layer_type
        )
