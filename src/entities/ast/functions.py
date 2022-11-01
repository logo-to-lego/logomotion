#pylint disable=fixme
from entities.ast.node import Node
from entities.logotypes import LogoType
from entities.symbol import Function, Variable


class Output(Node):
    def get_type(self):
        pass

    def check_types(self):
        pass


class ProcCall(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("ProcCall", children, leaf, **dependencies)

    def get_type(self):
        return self._logo_type

    def check_types(self):
        procedure = self._symbol_tables.functions.lookup(self.leaf)
        if not procedure:
            self._logger.error_handler.add_error(
                2019,
                proc=self.leaf,
                row=self.position.get_pos()[0]
            )
            return
        if len(procedure.parameters) != len(self.children):
            self._logger.error_handler.add_error(
                2020,
                proc=self.leaf,
                row=self.position.get_pos()[0],
                args=len(self.children),
                params=len(procedure.parameters)
            )
        for index in range(len(self.children)):
            self.children[index].check_types()
            if index >= len(procedure.parameters):
                continue
            argument_type = self.children[index].type
            parameter_type = procedure.parameters[index].type.value
            if argument_type != parameter_type:
                self._logger.error_handler.add_error(
                    2021,
                    proc=self.leaf,
                    arg=self.children[index].leaf,
                    atype=argument_type,
                    ptype=parameter_type,
                    row=self.position.get_pos()[0]
                )


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
        self._symbol_tables.functions.insert(self.leaf, Function(self.leaf))
        procedure = self._symbol_tables.functions.lookup(self.leaf)
        self._symbol_tables.variables.initialize_scope(in_function=procedure)
        for child in self.children:
            child.check_types()
        for parameter in procedure.parameters:
            if parameter.type == LogoType.UNKNOWN:
                self._logger.error_handler.add_error(
                    2018,
                    proc=procedure.name,
                    param=parameter.name)

        # funktion palautustyypin määrittäminen TODO

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
        procedure = self._symbol_tables.variables.get_in_scope_function_symbol()
        if self._symbol_tables.variables.lookup(self.leaf):
            self._logger.error_handler.add_error(2017, proc=procedure.name, param=self.leaf)
        variable = Variable(self.leaf)
        procedure.parameters.append(variable)
        self._symbol_tables.variables.insert(self.leaf, variable)
