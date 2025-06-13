from IR.IRContext import Variable
from IR.IRNodes import Identifier
from IR.IRParamValueGenerator import IRParamValueGenerator
from IR.layers.Globals import Global
from schema.SchemaClass import MethodInfo
from IR.IRNodes import CallExpression, Literal
from schema.SchemaClass import IDBType
import random


class PipeEnd:
    def __init__(self, method_info: MethodInfo):
        self.name = method_info.name
        self.method_info = method_info
        self.is_read = self._infer_is_read()
        self.is_write = self._infer_is_write()

    def _infer_is_read(self):
        return self.name in {"get", "getAll", "getAllKeys", "getKey", "count", "openCursor", "openKeyCursor"}

    def _infer_is_write(self):
        return self.name in {"put", "add", "delete", "clear"}

    def generate_il(self, store_id: Identifier, key, ):
        """
        基于 MethodInfo + IDBType + IRContext + LiteralContext 生成 CallExpression。
        自动将结果注册进 irctx（使用 returns 推导类型）。
        """
        args = IRParamValueGenerator.generateMethodArgs(method= self.method_info)

        result_name = Global.irctx.generate_unique_name(f"req_{self.name}")
        call = CallExpression(store_id, self.name, args, result_name=result_name)

        # 注册返回变量
        return_type = self.method_info.returns
        if isinstance(return_type, dict) and "typename" in return_type:
            return_typename = return_type["typename"]
        elif isinstance(return_type, str):
            return_typename = return_type
        else:
            return_typename = IDBType.IDBRequest.value

        Global.irctx.register_variable(Variable(name=result_name, type_=return_typename))
        return call

    def __repr__(self):
        return f"PipeEnd({self.name})"