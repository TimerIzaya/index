from typing import Any
from .base_interface import Interface, MethodSignature, Parameter

idb_factory_interface = Interface()

# ✅ 静态方法
idb_factory_interface.add_static_method(MethodSignature(
    name="open",
    parameters=[Parameter("name", str), Parameter("version", int)],
    return_type="IDBOpenDBRequest"
))

idb_factory_interface.add_static_method(MethodSignature(
    name="deleteDatabase",
    parameters=[Parameter("name", str)],
    return_type="IDBOpenDBRequest"
))

idb_factory_interface.add_static_method(MethodSignature(
    name="cmp",
    parameters=[Parameter("first", Any), Parameter("second", Any)],
    return_type=int
))
