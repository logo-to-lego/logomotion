from entities.ast.node import Node
from entities.logotypes import LogoType


class If(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("If", children, leaf, **dependencies)

    def get_logotype(self):
        return None

    def check_types(self):
        if self.leaf.get_logotype() is not LogoType.BOOL:
            self._logger.error_handler.add_error(
                "conditional_statement_does_not_return_boolean",
                self.position.get_lexspan()
            )
        self.leaf.check_types()
        self._symbol_tables.variables.initialize_scope()
        self.children[0].check_types()
        for variable in self.undefined_variables():
            self._logger.error_handler.add_error("undefined_variable", self.position.get_lexspan(), var=variable)
        self._symbol_tables.variables.finalize_scope()

    def generate_code(self):
        """Generate if statement to Java"""
        condition = self.leaf.generate_code()
        self._code_generator.if_statement(condition)
        for child in self.children:
            child.generate_code()
        self._code_generator.closing_brace()


class IfElse(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("IfElse", children, leaf, **dependencies)

    def get_logotype(self):
        return None

    def check_types(self):
        if self.leaf.get_logotype() is not LogoType.BOOL:
            self._logger.error_handler.add_error(
                "conditional_statement_does_not_return_boolean",
                self.position.get_lexspan()
            )
        self.leaf.check_types()
        self._symbol_tables.variables.initialize_scope()
        self.children[0].check_types()
        for variable in self.undefined_variables():
            self._logger.error_handler.add_error("undefined_variable", self.position.get_lexspan(), var=variable)
        self._symbol_tables.variables.finalize_scope()

        self._symbol_tables.variables.initialize_scope()
        self.children[1].check_types()
        for variable in self.undefined_variables():
            self._logger.error_handler.add_error("undefined_variable", self.position.get_lexspan(), var=variable)
        self._symbol_tables.variables.finalize_scope()

    def generate_code(self):
        condition = self.leaf.generate_code()
        self._code_generator.if_statement(condition)
        self.children[0].generate_code()
        self._code_generator.closing_brace()
        self._code_generator.else_statement()
        self.children[1].generate_code()
        self._code_generator.closing_brace()
