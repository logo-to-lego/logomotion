from entities.ast.node import Node


class Block(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("Block", children, None, **dependencies)

    def check_types(self):
        """Runs the check in given order."""
        for child in self.children:
            child.get_logotype()
            child.check_types()
