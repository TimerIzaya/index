from typing import Any
from .base_interface import Interface, MethodSignature, Parameter, InstanceProperty, EventListener

idb_transaction_interface = Interface()

# ✅ 实例方法
idb_transaction_interface.add_instance_method(MethodSignature(
    name="objectStore",
    parameters=[Parameter("name", str)],
    return_type="IDBObjectStore"
))

idb_transaction_interface.add_instance_method(MethodSignature(
    name="abort",
    parameters=[],
    return_type=None
))

# ✅ 实例属性
idb_transaction_interface.add_instance_property(InstanceProperty("db", "IDBDatabase", None))
idb_transaction_interface.add_instance_property(InstanceProperty("mode", str, "readonly"))
idb_transaction_interface.add_instance_property(InstanceProperty("objectStoreNames", Any, []))

# ✅ 事件监听
idb_transaction_interface.add_event_listener(EventListener(name="oncomplete", callback_type=Any))
idb_transaction_interface.add_event_listener(EventListener(name="onerror", callback_type=Any))
idb_transaction_interface.add_event_listener(EventListener(name="onabort", callback_type=Any))
