from typing import Any
from .base_interface import Interface, InstanceProperty
from .IDBCursor import idb_cursor_interface  # 继承 IDBCursor

idb_cursor_with_value_interface = Interface(
    instance_methods=idb_cursor_interface.instance_methods.copy(),
    instance_properties=idb_cursor_interface.instance_properties.copy(),
)

# ✅ `IDBCursorWithValue` 额外增加的属性
idb_cursor_with_value_interface.add_instance_property(InstanceProperty("value", Any, None))
