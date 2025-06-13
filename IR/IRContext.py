import random
from typing import List, Dict, Optional
from IR.IRNodes import Identifier, Variable
from IR.layers.Layer import Layer
from schema.SchemaClass import IDBType


class LayerPool:
    def __init__(self, layer: Layer):
        self.layer: Layer = layer
        self.vars: List[Variable] = []

    def append(self, v: Variable):
        self.vars.append(v)

class IRContext:
    def __init__(self):
        #作用域栈
        self.layerStack: List[LayerPool] = []
        self.unique_counter = 0

    def enter_layer(self, layer):
        self.layerStack.append(LayerPool(layer))

    def exit_layer(self):
        self.layerStack.pop()

    def register_variable(self, var: Variable):
        assert isinstance(var, Variable), "register_variable() must be called with a Variable instance"
        self.layerStack[-1].append(var)

    def get_random_identifier(self, typename: IDBType) -> Identifier:
        for layPool in self.layerStack:
            for v in layPool.vars:
                if v.type.typename == typename:
                    return v.name
        raise ValueError(f"No identifier found for type {typename}")

    def get_visible_variables(self, typename: IDBType) -> List[Variable]:
        result = []
        for layPool in self.layerStack:
            for v in layPool.vars:
                if v.type == typename:
                    result.append(v)
        return result

    def get_identifier_by_type(self, type_: IDBType) -> Optional[Identifier]:
        candidates = []
        for layPool in self.layerStack:
            for v in layPool.vars:
                if v.type == type_:
                    candidates.append(v)
        return random.choice(candidates) if candidates else None

    def generate_unique_name(self, base: str) -> str:
        name = f"{base}_{self.unique_counter}"
        self.unique_counter += 1
        return name
