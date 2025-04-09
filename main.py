import json
import os
from pathlib import Path

from IR.IRFuzzer import loadFuzzerNeed, generate_ir_program
from IR.IRNodes import Program
from lifter.IRToJSLifter import IRToJSLifter

if __name__ == "__main__":
    loadFuzzerNeed()
    program = generate_ir_program()
    x = json.dumps(program.to_dict(), indent=2)
    file_path = "lifter/IRDemo.json"

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(x)

    input_path = Path("lifter/IRDemo.json")
    with open(input_path, "r") as f:
        ir_data = json.load(f)

    # 用于测试的 Program.from_dict (假设结构直接传递给 Program)
    program = Program.from_dict(ir_data)

    # 转换为 JS 源码
    converter = IRToJSLifter()
    js_code = converter.lift_program(program)

    # 输出
    print(js_code)
