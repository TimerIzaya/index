import random

from IR.IRContext import IRContext
from IR.IRType import Type


class IRParameterGenerator:
    def __init__(self, context: IRContext):
        self.context = context

    def generate_parameter(self, paramInSchema):
        param_type = Type(paramInSchema["type"])
        typename = param_type.typename()

        # 尝试复用已有变量
        candidates = self.context.get_visible_variables(typename)
        if candidates:
            return random.choice(candidates)

        # 否则新生成值（这里只是示例生成器）
        value = self._generate_by_type(typename)
        var_name = self._generate_variable_name(typename)
        self.context.register_variable(var_name, typename)
        return var_name  # 实际 fuzz 可返回更复杂表达式

    def _generate_by_type(self, typename):
        if typename == "string":
            return f'"str_{random.randint(0, 100)}"'
        elif typename == "number":
            return random.randint(0, 100)
        elif typename == "boolean":
            return random.choice(["true", "false"])
        else:
            return f'{typename}_instance'

    def _generate_variable_name(self, typename):
        return f'{typename}_{random.randint(0, 9999)}'


if __name__ == '__main__':
    ctx = IRContext()
    gen = IRParameterGenerator(ctx)

    ctx.enter_layer("OpenDatabase")
    print("[Add db]", gen.generate_parameter({"name": "db", "type": "string"}))

    ctx.enter_layer("Transaction")
    print("[Reuse or add storeNames]", gen.generate_parameter({"name": "storeNames", "type": [
        {Consts.TypeName: "string"},
        {Consts.TypeName: "array"}
    ]}))

    ctx.exit_layer()
    ctx.debug()
