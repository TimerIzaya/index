from typing import Any
from .base_interface import Interface, MethodSignature, Parameter, InstanceProperty

idb_key_range_interface = Interface()

# ✅ 静态方法
idb_key_range_interface.add_static_method(MethodSignature(
    name="only",
    parameters=[Parameter("value", Any)],
    return_type="IDBKeyRange"
))

idb_key_range_interface.add_static_method(MethodSignature(
    name="lowerBound",
    parameters=[Parameter("lower", Any), Parameter("openLower", bool)],
    return_type="IDBKeyRange"
))

idb_key_range_interface.add_static_method(MethodSignature(
    name="upperBound",
    parameters=[Parameter("upper", Any), Parameter("openUpper", bool)],
    return_type="IDBKeyRange"
))

idb_key_range_interface.add_static_method(MethodSignature(
    name="bound",
    parameters=[
        Parameter("lower", Any),
        Parameter("upper", Any),
        Parameter("openLower", bool),
        Parameter("openUpper", bool)
    ],
    return_type="IDBKeyRange"
))

# ✅ 实例方法
idb_key_range_interface.add_instance_method(MethodSignature(
    name="includes",
    parameters=[Parameter("key", Any)],
    return_type=bool
))

# ✅ 实例属性
idb_key_range_interface.add_instance_property(InstanceProperty("lower", Any, None))
idb_key_range_interface.add_instance_property(InstanceProperty("upper", Any, None))
idb_key_range_interface.add_instance_property(InstanceProperty("lowerOpen", bool, False))
idb_key_range_interface.add_instance_property(InstanceProperty("upperOpen", bool, False))
