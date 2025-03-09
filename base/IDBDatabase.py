from typing import Any
from .base_interface import Interface, MethodSignature, Parameter, InstanceProperty, EventListener

idb_database_interface = Interface()

# ✅ 实例方法
idb_database_interface.add_instance_method(MethodSignature(
    name="createObjectStore",
    parameters=[Parameter("name", str), Parameter("options", Any)],
    return_type="IDBObjectStore"
))

idb_database_interface.add_instance_method(MethodSignature(
    name="deleteObjectStore",
    parameters=[Parameter("name", str)],
    return_type=None
))

idb_database_interface.add_instance_method(MethodSignature(
    name="transaction",
    parameters=[Parameter("storeNames", Any), Parameter("mode", str)],
    return_type="IDBTransaction"
))

idb_database_interface.add_instance_method(MethodSignature(
    name="close",
    parameters=[],
    return_type=None
))

# ✅ 实例属性
idb_database_interface.add_instance_property(InstanceProperty("name", str, ""))
idb_database_interface.add_instance_property(InstanceProperty("version", int, 1))
idb_database_interface.add_instance_property(InstanceProperty("objectStoreNames", Any, []))

# ✅ 事件监听
idb_database_interface.add_event_listener(EventListener(name="onversionchange", callback_type=Any))
