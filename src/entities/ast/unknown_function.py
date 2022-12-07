from entities.ast.node import Node
from entities.logotypes import LogoType

class UnknownFunction(Node):
    """
    Args:
        arg_type: either a LogoType or False.
        param_specs: for loop iter information passed from proccall
    """
    def __init__(self, children=None, **dependencies):
        super().__init__("UnknownFunction", children, None, **dependencies)
        self.var_node = None

    def get_logotype(self) -> LogoType:
        return LogoType.NAMELESS_FUNCTION

    def check_types(self):
        self._symbol_tables.variables.initialize_scope()
        if self.var_node:
            self.var_node.scoped_type_check()
        # if we're handling a for loop, we need to add the iterator to the scope
        for child in self.children:
            child.check_types()
        self._symbol_tables.variables.finalize_scope()

    def generate_code(self):
        """Generate block into for or repeat lambda-statement"""
        tmpvar = self._code_generator.lambda_no_param_start()
        for child in self.children:
            child.generate_code()
        self._code_generator.lambda_end()
        return tmpvar
