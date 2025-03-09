from typing import Any
from .base_interface import Interface, EventListener

idb_open_db_request_interface = Interface()

# ✅ 事件监听
idb_open_db_request_interface.add_event_listener(EventListener(name="onblocked", callback_type=Any))
idb_open_db_request_interface.add_event_listener(EventListener(name="onupgradeneeded", callback_type=Any))
