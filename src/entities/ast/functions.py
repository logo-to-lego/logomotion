from entities.ast.node import Node
from entities.logotypes import LogoType
from entities.symbol import *


class Output(Node):
    def get_type(self):
        pass

    def check_types(self):
        pass


class Command(Node):
    pass


class ProcDecl(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("ProcDecl", children, leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.UNKNOWN

        return self._logo_type

    def check_types(self):
        if self._symbol_tables.functions.lookup(self.leaf):
            self._logger.error_handler.add_error(2016, proc=self.leaf)
            self._logger.console.write(f"Procedure {self.leaf} already declared")
        else:
            self._symbol_tables.functions.insert(self.leaf, Function(self.leaf)) # lisää vielä loput argumentit
        self._symbol_tables.variables.initialize_scope(
            in_function=self._symbol_tables.functions.lookup(self.leaf)
        )
        for child in self.children:
            child.check_types()
        self._symbol_tables.variables.finalize_scope()


class ProcArgs(Node):
    def __init__(self, children, **dependencies):
        super().__init__("ProcArgs", children, **dependencies)

    def check_types(self):
        for child in self.children:
            child.check_types()

class ProcArg(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("ProgArg", children, **dependencies)

    def check_types(self):
        self._symbol_tables.variables.insert(self.leaf, Variable(self.leaf, logotype=LogoType.UNKNOWN))
