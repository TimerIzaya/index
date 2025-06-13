# from typing import Dict
#
# from IR.IRType import Type
#
#
# class IRTypeRegistry:
#     def __init__(self):
#         self.types: Dict[str, Type] = {}
#
#     def register(self, name: str):
#         if name not in self.types:
#             self.types[name] = Type(name)
#
#     def get_all(self):
#         return self.types
