from IR.IRContext import IRContext, Variable
from IR.IRType import IDBFactory, IDBDatabase
from IR.IRNodes import VariableDeclaration
from layers.IDBContext import IDBContext
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.IDBFactory_OpenDatabase_Layer import IDBFactory_OpenDatabase_Layer


class IDBRootLayer(LayerBuilder):

    name = "IDBRootLayer"

    layer_type = LayerType.CALLING

    @staticmethod
    def build(irctx: IRContext, idbctx: IDBContext) -> Layer:
        # 注册 indexedDB 对象
        irctx.register_variable(Variable("window.indexedDB", IDBFactory))

        # ✅ 全局声明 db 变量
        irctx.register_variable(Variable("db", IDBDatabase))
        db_decl = VariableDeclaration("let", "db")

        # 构造 open 层
        open_layer = IDBFactory_OpenDatabase_Layer.build(irctx, idbctx)

        # 生成 Root 层结构
        return Layer(
            IDBRootLayer.name,
            ir_nodes=[db_decl],
            children=[open_layer],
            layer_type=IDBRootLayer.layer_type
        )
