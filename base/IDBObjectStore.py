from typing import Any
from .base_interface import Interface, MethodSignature, Parameter, InstanceProperty

idb_object_store_interface = Interface()

# ✅ 实例方法
idb_object_store_interface.add_instance_method(MethodSignature(
    name="add",
    parameters=[Parameter("value", Any), Parameter("key", Any)],
    return_type="IDBRequest"
))

idb_object_store_interface.add_instance_method(MethodSignature(
    name="put",
    parameters=[Parameter("value", Any), Parameter("key", Any)],
    return_type="IDBRequest"
))

idb_object_store_interface.add_instance_method(MethodSignature(
    name="get",
    parameters=[Parameter("key", Any)],
    return_type="IDBRequest"
))

idb_object_store_interface.add_instance_method(MethodSignature(
    name="delete",
    parameters=[Parameter("key", Any)],
    return_type="IDBRequest"
))

idb_object_store_interface.add_instance_method(MethodSignature(
    name="clear",
    parameters=[],
    return_type="IDBRequest"
))

idb_object_store_interface.add_instance_method(MethodSignature(
    name="openCursor",
    parameters=[Parameter("query", Any), Parameter("direction", str)],
    return_type="IDBRequest"
))

# ✅ 实例属性
idb_object_store_interface.add_instance_property(InstanceProperty("name", str, ""))
idb_object_store_interface.add_instance_property(InstanceProperty("keyPath", Any, None))
idb_object_store_interface.add_instance_property(InstanceProperty("autoIncrement", bool, False))
