from entities.ast.node import Node
from entities.logotypes import LogoType


class UnknownFunction(Node):
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
        tmpvar = self._code_generator.lambda_no_param_start()
        for child in self.children:
            child.generate_code()
        self._code_generator.lambda_end()
        return tmpvar
