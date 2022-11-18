from entities.ast.functions import Output
from entities.ast.node import Node


class StatementList(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("StatementList", children, None, **dependencies)

    def check_types(self):
        """Runs the check in given order."""
        for index, child in enumerate(self.children):
            child.get_logotype()
            child.check_types()

            # Check output statement ends statement list
            if child.__class__ == Output:
                procedure = self._symbol_tables.variables.get_in_scope_function_symbol()
                if procedure and index != len(self.children) - 1:
                    self._logger.error_handler.add_error(
                        2027,
                        proc=procedure.name
                    )
