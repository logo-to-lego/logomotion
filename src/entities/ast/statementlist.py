from entities.ast.node import Node


class StatementList(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("StatementList", children, None, **dependencies)

    def check_types(self):
        """Runs the check in given order."""
        for child in self.children:
            child.get_logotype()
            child.check_types()
