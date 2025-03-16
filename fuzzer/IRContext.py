class IRContext:
    """
    维护当前 IR 生成状态。
    - 记录已定义变量，防止非法调用
    - 确保事务 `tx` 不能在 `onsuccess` 之外创建
    - 跟踪 IndexedDB 数据库和对象存储状态
    """
    def __init__(self):
        self.variables = {}  # name -> type
        self.transactions = []  # 记录事务状态
        self.current_db = None  # 记录当前数据库名称

    def register_variable(self, name, type_):
        self.variables[name] = type_

    def is_variable_defined(self, name):
        return name in self.variables

    def enter_transaction(self, tx_name):
        self.transactions.append(tx_name)

    def exit_transaction(self):
        if self.transactions:
            self.transactions.pop()

    def has_active_transaction(self):
        return bool(self.transactions)
