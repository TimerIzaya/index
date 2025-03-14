# const request = indexedDB.open("mydb", 1);
# request.onsuccess = function(event) {
#   const db = event.target.result;
#   const store = db.createObjectStore("store1");
# };


from IR.CallExpression import CallExpression
from IR.FunctionBody import FunctionBody
from IR.MemberExpression import MemberExpression
from IR.Program import Program
from IR.VariableDeclaration import VariableDeclaration

program = Program()

# Step 1: indexedDB.open("mydb", 1)
open_call = CallExpression("indexedDB", "open", ["mydb", 1], result_name="request")

# Step 2: onsuccess 回调体
onsuccess = FunctionBody(params=["event"])
var_db = VariableDeclaration("db", MemberExpression("event.target", "result"))
call_store = CallExpression("db", "createObjectStore", ["store1"], result_name="store")
onsuccess.body.extend([var_db, call_store])

# Step 3: 添加 handler 到 open 请求
open_call.add_handler("onsuccess", onsuccess)

# Step 4: 加入 program
program.add(open_call)

# 打印结构
import json
print(json.dumps(program.to_dict(), indent=2))
