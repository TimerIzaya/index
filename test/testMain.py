import unittest

from IR.IRContext import IRContext
from IR.IRParamValueGenerator import IRParamValueGenerator
from schema.IDBSchemaParser import IDBSchemaParser
from schema.SchemaClass import IDBType, TypeInfo
from schema.SchemaInstanceTree import SchemaInstanceTree


class MyTestCase(unittest.TestCase):

    def testSchemaInstanceTree(self):
        tree = SchemaInstanceTree()
        tree.summary()
        tree.check_coverage()

    def testIDBSchemaParser(self):
        # 获取 open 方法的第一个参数类型
        t1 = IDBSchemaParser.getInterface("IDBFactory") \
            .getStaticMethod("open") \
            .getParam(0) \
            .getAttr("type")

        print("open param[0].type =", t1)

        # 获取 transaction 方法第一个参数（联合类型）
        t2 = IDBSchemaParser.getInterface("IDBDatabase") \
            .getInstanceMethod("transaction") \
            .getParam(0) \
            .getAttr("type")

        print("transaction param[0].type =", t2)

        # 获取 onversionchange 事件定义
        e1 = IDBSchemaParser.getInterface("IDBDatabase").getEvent("onversionchange")
        print("onversionchange =", e1)

        # 获取 put() 的返回类型
        ret = IDBSchemaParser.getInterface("IDBObjectStore") \
            .getInstanceMethod("put") \
            .getReturn() \
            .getAttr("typename")

        print("put return typename =", ret)

        ret = IDBSchemaParser.getInterface("IDBDatabase") \
            .getInstanceMethod("transaction") \
            .getParam("storeNames") \
            .getType()

        print("transaction param[0].storeNames =", ret)

        method = IDBSchemaParser.getInterface("IDBDatabase") \
            .getInstanceMethod("transaction") \

        print(1)


    def testParamGenerator(self):
        context = IRContext()
        generator = IRParamValueGenerator(context)

        print("==== TypeInfo Generation Test ====")
        for idb_type in IDBType:
            type_info = TypeInfo({"typename": idb_type.value})
            try:
                value = generator.generate_value_from_type(type_info)
                print(f"{idb_type.value:20} => {value}")
            except Exception as e:
                print(f"{idb_type.value:20} => Error: {str(e)}")

if __name__ == '__main__':
    unittest.main()
