from entities.ast.node import Node
from entities.logotypes import LogoType


class If(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("If", children, leaf, **dependencies)

    def get_logotype(self):
        return None

    def check_types(self):
        if self.leaf.get_logotype() is not LogoType.BOOL:
            self._logger.error_handler.add_error(2006, row=self.position.get_pos()[0])
        self.leaf.check_types()
        self._symbol_tables.variables.initialize_scope()
        self.children[0].check_types()
        for variable in self.undefined_variables():
            self._logger.error_handler.add_error(2007, var=variable)
        self._symbol_tables.variables.finalize_scope()

    def generate_code(self):
        """Generate if statement to Java"""
        condition = self.leaf.generate_code()
        self._code_generator.if_statement(condition)
        for child in self.children:
            child.generate_code()
        self._code_generator.closing_brace()
        # Lambda method. Delete code above and uncomment below if in use
        #codition = self.leaf.generate_code()
        #lambda_var = self._code_generator.lambda_no_param_start()
        #for child in self.children:
        #    child.generate_code()
        #self._code_generator.lambda_end()
        #self._code_generator.if_statement_lambda(condition, lambda_var)


class IfElse(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("IfElse", children, leaf, **dependencies)

    def get_logotype(self):
        return None

    def check_types(self):
        if self.leaf.get_logotype() is not LogoType.BOOL:
            self._logger.error_handler.add_error(2006, row=self.position.get_pos()[0])
        self.leaf.check_types()
        self._symbol_tables.variables.initialize_scope()
        for child in self.children:
            child.check_types()
        for variable in self.undefined_variables():
            self._logger.error_handler.add_error(2007, var=variable)
        self._symbol_tables.variables.finalize_scope()
