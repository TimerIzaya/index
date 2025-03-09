from typing import Any
from .base_interface import Interface, InstanceProperty, EventListener

idb_request_interface = Interface()

# ✅ 实例属性
idb_request_interface.add_instance_property(InstanceProperty("result", Any, None))
idb_request_interface.add_instance_property(InstanceProperty("error", Any, None))
idb_request_interface.add_instance_property(InstanceProperty("source", Any, None))
idb_request_interface.add_instance_property(InstanceProperty("transaction", Any, None))
idb_request_interface.add_instance_property(InstanceProperty("readyState", str, "pending"))

# ✅ 事件监听
idb_request_interface.add_event_listener(EventListener(name="onsuccess", callback_type=Any))
idb_request_interface.add_event_listener(EventListener(name="onerror", callback_type=Any))
