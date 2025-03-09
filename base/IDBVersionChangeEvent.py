from typing import Any
from .base_interface import Interface, InstanceProperty

idb_version_change_event_interface = Interface()

# ✅ 实例属性
idb_version_change_event_interface.add_instance_property(InstanceProperty("oldVersion", int, 0))
idb_version_change_event_interface.add_instance_property(InstanceProperty("newVersion", Any, None))
