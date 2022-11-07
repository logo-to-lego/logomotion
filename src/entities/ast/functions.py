from entities.ast.node import Node


class Output(Node):
    def get_logotype(self):
        pass

    def check_types(self):
        pass


class Command(Node):
    pass


class ProcDecl(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("ProcDecl", children, leaf, **dependencies)

    def get_logotype(self):
        return None

    def check_types(self):
        if self._symbol_tables.functions.lookup(self.leaf):
            self._logger.console.write(f"Procedure {self.leaf} already declared")
        self._symbol_tables.variables.initialize_scope()
        for child in self.children:
            child.check_types()
        self._symbol_tables.variables.finalize_scope()


class ProcArgs(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("ProcArgs", children, **dependencies)

    def check_types(self):
        for child in self.children:
            child.check_types()
