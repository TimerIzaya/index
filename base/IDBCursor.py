from typing import Any
from .base_interface import Interface, MethodSignature, Parameter, InstanceProperty

idb_cursor_interface = Interface()

# ✅ 实例方法（适用于 IDBCursor 和 IDBCursorWithValue）
idb_cursor_interface.add_instance_method(MethodSignature(
    name="advance",
    parameters=[Parameter("count", int)],
    return_type=None
))

idb_cursor_interface.add_instance_method(MethodSignature(
    name="continue",
    parameters=[Parameter("key", Any)],
    return_type=None
))

idb_cursor_interface.add_instance_method(MethodSignature(
    name="delete",
    parameters=[],
    return_type="IDBRequest"
))

# ✅ 实例属性（适用于 IDBCursor 和 IDBCursorWithValue）
idb_cursor_interface.add_instance_property(InstanceProperty("key", Any, None))
idb_cursor_interface.add_instance_property(InstanceProperty("primaryKey", Any, None))
idb_cursor_interface.add_instance_property(InstanceProperty("direction", str, "next"))
