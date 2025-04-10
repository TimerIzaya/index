import random
from typing import List, Dict, Optional
from IR.IRNodes import Identifier
from IR.IRType import Type


class Variable:
    def __init__(self, name: str, type_: Type):
        self.name = name
        self.type = type_

    def __repr__(self):
        return f"<Variable {self.name}: {self.type.typename}>"

class IRContext:
    def __init__(self):
        self.scopes: List[Dict[str, Variable]] = [{}]
        self.layer_stack: List[str] = []

    def enter_layer(self, layer):
        self.scopes.append({})
        self.layer_stack.append(layer.name if hasattr(layer, "name") else str(layer))

    def exit_layer(self):
        self.scopes.pop()
        self.layer_stack.pop()

    def register_variable(self, var: Variable):
        assert isinstance(var, Variable), "register_variable() must be called with a Variable instance"
        self.scopes[-1][var.name] = var

    def get_random_identifier(self, typename: str) -> Identifier:
        for scope in reversed(self.scopes):
            for var in scope.values():
                if var.type.typename == typename:
                    return Identifier(var.name)
        raise ValueError(f"No identifier found for type {typename}")

    def get_visible_variables(self, typename: str) -> List['Variable']:
        result = []
        for scope in reversed(self.scopes):
            for var in scope.values():
                if var.type.typename == typename:
                    result.append(var)
        return result

    def get_identifier_by_type(self, type_: Type) -> Optional[Identifier]:
        candidates = []
        for scope in reversed(self.scopes):
            for var in scope.values():
                if var.type == type_:
                    candidates.append(Identifier(var.name))
        return random.choice(candidates) if candidates else None
