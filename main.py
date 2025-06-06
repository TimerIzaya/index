import json
import os
from pathlib import Path

from IR.IRFuzzer import  generate_ir_program
from IR.layers.Layer import Layer
from lifter.IRToJSLifter import IRToJSLifter

if __name__ == "__main__":
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

    # lifter
    with open("lifter/IRDemo.json", "r") as f:
        ir_data = json.load(f)

    root_layer = Layer.from_dict(ir_data)
    lines = IRToJSLifter._convert_layer(root_layer, 0)
    print("\n".join(lines))