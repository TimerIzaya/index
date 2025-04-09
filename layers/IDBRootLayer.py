from IR.IRContext import IRContext, Variable
from IR.IRType import IDBFactory, IDBDatabase
from IR.IRNodes import VariableDeclaration
from layers.Layer import Layer, LayerType
from layers.LayerBuilder import LayerBuilder
from layers.IDBFactory_OpenDatabase_Layer import IDBFactory_OpenDatabase_Layer


class IDBRootLayer(LayerBuilder):
    name = "IDBRootLayer"
    layer_type = LayerType.CALLING

    @staticmethod
    def build(ctx: IRContext) -> Layer:
        # 注册 indexedDB 对象
        ctx.register_variable(Variable("window.indexedDB", IDBFactory))

        # ✅ 全局声明 db 变量
        ctx.register_variable(Variable("db", IDBDatabase))
        db_decl = VariableDeclaration("let", "db")

        # 构造 open 层
        open_layer = IDBFactory_OpenDatabase_Layer.build(ctx)

        # 生成 Root 层结构
        return Layer(
            IDBRootLayer.name,
            ir_nodes=[db_decl],         # ✅ 插入 let db;
            children=[open_layer],
            layer_type=IDBRootLayer.layer_type
        )
