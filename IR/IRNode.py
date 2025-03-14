class IRNode:
    def to_dict(self) -> dict:
        raise NotImplementedError()

    def __repr__(self):
        return str(self.to_dict())
