from entities.ast.node import Node
from entities.logotypes import LogoType


class Block(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("Block", children, None, **dependencies)

    def get_logotype(self) -> LogoType:
        return LogoType.NAMELESS_FUNCTION

    def check_types(self):
        """Runs the check in given order."""
        for child in self.children:
            child.get_logotype()
            child.check_types()

    def generate_code(self):
        """Generate block into for statement"""
        aaa = 1+1 #debug
        return aaa
