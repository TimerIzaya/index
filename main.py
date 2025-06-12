import json
import os
import shutil
from pathlib import Path

from IR.IRFuzzer import  generate_ir_program
from IR.layers.Layer import Layer
from lifter.IRToJSLifter import IRToJSLifter



def resetCorpus():
    corpus_dir = "./corpus"

    # 删除目录（包括内容）
    if os.path.exists(corpus_dir):
        shutil.rmtree(corpus_dir)
        print("Deleted existing corpus directory.")

    # 重新创建空目录
    os.makedirs(corpus_dir)
    print("Recreated empty corpus directory.")

def genCase(number):
    IR = generate_ir_program()
    IRJson = json.dumps(IR.to_dict(), indent=2)
    IRPath = f"corpus/{number}.json"
    JSPath = f"corpus/{number}.js"

    if os.path.exists(IRPath):
        os.remove(IRPath)

    with open(IRPath, "w", encoding="utf-8") as f:
        f.write(IRJson)

    # 这里绕一圈是为了测试lifter相互转化的能力
    with open(IRPath, "r") as f:
        ir_data = json.load(f)

    root_layer = Layer.from_dict(ir_data)
    lines = IRToJSLifter.convertLayer(root_layer, 0)

    for line in lines:
        with open(JSPath, "a", encoding="utf-8") as f:
            f.write(line + "\n")


if __name__ == "__main__":
    resetCorpus()
    for i in range(0, 10):
        genCase(i)
