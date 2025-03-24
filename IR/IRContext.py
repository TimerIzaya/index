from typing import Dict, List, Optional, Union
from IR.IRNodes import Identifier
from IRType import Type

class Variable:
    def __init__(self, name: str, type_: Type):
        self.identifier = Identifier(name)  # 用于生成 IR 节点
        self.type = type_                   # Type 对象

    def __repr__(self):
        return f"<Variable name={self.identifier.name} type={self.type.typename}>"

class IRContext:
    def __init__(self):
        self.scopes: List[Dict[str, Variable]] = [{}]

    def enter_layer(self, layer_name: str):
        self.scopes.append({})

    def exit_layer(self):
        self.scopes.pop()

    def register_variable(self, name: str, type_: Union[Type, str]):
        # 自动转换为 Type 实例
        if isinstance(type_, str):
            from config import AllIRTypes
            type_ = AllIRTypes.get(type_, Type(type_))
        var = Variable(name, type_)
        self.scopes[-1][name] = var

    def get_visible_variables(self, type_: Optional[Union[Type, str]] = None) -> List[Variable]:
        found = []
        for scope in reversed(self.scopes):
            for var in scope.values():
                if type_ is None:
                    found.append(var)
                elif isinstance(type_, str) and var.type.typename == type_:
                    found.append(var)
                elif isinstance(type_, Type) and var.type.typename == type_.typename:
                    found.append(var)
        return found

    def get_random_identifier(self, type_: Optional[Union[Type, str]] = None) -> Identifier:
        candidates = self.get_visible_variables(type_)
        if not candidates:
            raise ValueError(f"No variable of type {type_} found in context")
        import random
        return random.choice(candidates).identifier
