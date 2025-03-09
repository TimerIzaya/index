from typing import List, Dict, Type, Any
from dataclasses import dataclass, field

@dataclass
class Parameter:
    """表示方法的参数"""
    name: str
    param_type: Type[Any]

@dataclass
class MethodSignature:
    """表示方法签名"""
    name: str
    parameters: List[Parameter]
    return_type: Type[Any]
    is_static: bool = False

@dataclass
class InstanceProperty:
    """表示实例属性"""
    name: str
    property_type: Type[Any]
    default_value: Any = None

@dataclass
class EventListener:
    """表示一个事件监听器"""
    name: str
    callback_type: Type[Any]

@dataclass
class Interface:
    """表示 IndexedDB API 接口"""
    instance_methods: Dict[str, MethodSignature] = field(default_factory=dict)
    static_methods: Dict[str, MethodSignature] = field(default_factory=dict)
    instance_properties: Dict[str, InstanceProperty] = field(default_factory=dict)
    event_listeners: Dict[str, EventListener] = field(default_factory=dict)

    def add_instance_method(self, method: MethodSignature):
        self.instance_methods[method.name] = method

    def add_static_method(self, method: MethodSignature):
        method.is_static = True
        self.static_methods[method.name] = method

    def add_instance_property(self, prop: InstanceProperty):
        self.instance_properties[prop.name] = prop

    def add_event_listener(self, event: EventListener):
        self.event_listeners[event.name] = event
