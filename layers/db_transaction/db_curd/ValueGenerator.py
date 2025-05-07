import random
import string


class ValueGenerator:
    # === 可配置参数区域 ===
    DEFAULT_MAX_DEPTH = 3          # 对象最大嵌套深度
    DEFAULT_MAX_FIELDS = 10        # 每层对象最多字段数
    DEFAULT_STRING_MIN_LEN = 3     # 随机字符串最小长度
    DEFAULT_STRING_MAX_LEN = 12    # 随机字符串最大长度
    ANY_TYPE_DISTRIBUTION = (
        ["object"] * 5 +           # "any" 类型中 object 的权重更大
        ["string", "number", "boolean", "null", "array"]
    )
    # ======================

    def __init__(self):
        self.max_depth = self.DEFAULT_MAX_DEPTH
        self.max_fields = self.DEFAULT_MAX_FIELDS

    def generate(self, typename: str, key=None):
        method = getattr(self, f"generate_{typename}", None)
        if method:
            return method(key)
        return f"<{typename}>"

    def generate_string(self, key=None):
        return self._random_string()

    def generate_number(self, key=None):
        return key if key is not None else random.randint(0, 100)

    def generate_boolean(self, key=None):
        return random.choice([True, False])

    def generate_null(self, key=None):
        return None

    def generate_array(self, key=None):
        return [self._generate_primitive() for _ in range(random.randint(1, 3))]

    def generate_object(self, key=None):
        obj = self._generate_object()
        if key is not None:
            obj["id"] = key
        return obj

    def generate_any(self, key=None):
        chosen = random.choice(self.ANY_TYPE_DISTRIBUTION)
        return self.generate(chosen, key=key)

    def generate_function(self, key=None):
        return "(e) => {}"

    def _generate_object(self, current_depth=0):
        if current_depth >= self.max_depth:
            return self._generate_primitive()
        obj = {}
        field_count = random.randint(1, self.max_fields)
        for i in range(field_count):
            field_name = self._random_field_name(i)
            obj[field_name] = self._generate_value(current_depth)
        return obj

    def _generate_value(self, current_depth):
        t = random.choice(["string", "number", "boolean", "null", "array", "object"])
        return self.generate(t)

    def _generate_primitive(self):
        return random.choice([
            self._random_string(),
            random.randint(0, 100),
            True, False, None
        ])

    def _random_string(self, min_length=DEFAULT_STRING_MIN_LEN, max_length=DEFAULT_STRING_MAX_LEN):
        length = random.randint(min_length, max_length)
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    def _random_field_name(self, index):
        return f"f{index}_{random.choice(string.ascii_lowercase)}"


# ✅ 简单测试
def main():
    valgen = ValueGenerator()

    print("generate_string:", valgen.generate_string())
    print("generate_number:", valgen.generate_number(key=123))
    print("generate_boolean:", valgen.generate_boolean())
    print("generate_null:", valgen.generate_null())
    print("generate_array:", valgen.generate_array())
    print("generate_object:", valgen.generate_object(key=123))
    print("generate_any:", valgen.generate_any(key=123))
    print("generate_function:", valgen.generate_function())

if __name__ == "__main__":
    main()
