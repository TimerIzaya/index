from typing import Any
from .base_interface import Interface, MethodSignature, Parameter, InstanceProperty

idb_index_interface = Interface()

# ✅ 实例方法
idb_index_interface.add_instance_method(MethodSignature(
    name="get",
    parameters=[Parameter("key", Any)],
    return_type="IDBRequest"
))

idb_index_interface.add_instance_method(MethodSignature(
    name="getAll",
    parameters=[Parameter("query", Any)],
    return_type="IDBRequest"
))

idb_index_interface.add_instance_method(MethodSignature(
    name="count",
    parameters=[Parameter("query", Any)],
    return_type="IDBRequest"
))

# ✅ 实例属性
idb_index_interface.add_instance_property(InstanceProperty("name", str, ""))
idb_index_interface.add_instance_property(InstanceProperty("unique", bool, False))
idb_index_interface.add_instance_property(InstanceProperty("multiEntry", bool, False))
