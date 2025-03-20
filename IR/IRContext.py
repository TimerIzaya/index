class IRContext:
    def __init__(self):
        self.scopes = []  # List of {"layer": str, "variables": [ {"name": str, "type": str} ]}

    def enter_layer(self, layer_name: str):
        self.scopes.append({"layer": layer_name, "variables": []})

    def exit_layer(self):
        if self.scopes:
            self.scopes.pop()

    def register_variable(self, name: str, type_: str):
        if not self.scopes:
            raise RuntimeError("No active layer scope to register variable")
        self.scopes[-1]["variables"].append({"name": name, "type": type_})

    def get_visible_variables(self, type_: str):
        visible = []
        for scope in reversed(self.scopes):
            visible.extend([v["name"] for v in scope["variables"] if v["type"] == type_])
        return visible

    def debug(self):
        print("=== IRContext ===")
        for scope in self.scopes:
            print(f"Layer: {scope['layer']}")
            for var in scope["variables"]:
                print(f"  - {var['name']} : {var['type']}")
