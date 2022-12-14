from entities.ast.node import Node
from entities.logotypes import LogoType

class UnknownFunction(Node):
    """
    Args:
        var_node: This is the iterator for 'for' command structure
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
        for child in self.children:
            child.check_types()
        self._symbol_tables.variables.finalize_scope()

    def _has_output(self, node):
        if node.node_type == "Output":
            return True
        for child in node.children:
            return self._has_output(child)
        return False

    def generate_code(self):
        """Generate unknown_function into a lambda-statement"""
        tmpvar = self._code_generator.lambda_no_param_start()
        for child in self.children:
            child.generate_code()
        if not self._has_output(self):
            self._code_generator.return_null()
        self._code_generator.lambda_end()
        # in case we have multiple loops with same name for the iterator variable,
        # we'll remove the variable from known variable names, so that they won't overlap
        if self.var_node:
            self._code_generator.remove_java_variable_name(self.var_node.leaf.leaf)
        return self._code_generator.callable(tmpvar)
