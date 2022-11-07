#pylint disable=fixme
from entities.ast.node import Node
from entities.logotypes import LogoType
from entities.symbol import Function, Variable


class Output(Node):
    def get_type(self):
        pass

    def check_types(self):
        self.children[0].check_types()
        output_value = self.children[0]
        procedure = self._symbol_tables.variables.get_in_scope_function_symbol()
        if not procedure:
            # virhe: ei olla funktion sisällä
            self._logger.error_handler.add_error(2024, row=self.position.get_pos()[0])
            return
        if procedure.get_logotype() == LogoType.UNKNOWN:
            # aseta funktion tyypiksi palautusarvon tyyppi
            if output_value.type == "Deref"
            procedure.typeclass.logotype = output_value.get_type()
        else:
            # tarkista, että palautustyyppi on sama
            if procedure.get_logotype() != output_value.get_type():
                # virhe: funktion palautusarvo ei ole oikeaa, jo aiemmin määriteltyä tyyppiä
                self._logger.error_handler.add_error(2025, proc=procedure.name)


class ProcCall(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("ProcCall", children, leaf, **dependencies)

    def check_types(self):
        # Check the procedure has been declarated
        procedure = self._symbol_tables.functions.lookup(self.leaf)
        if not procedure:
            self._logger.error_handler.add_error(
                2020,
                proc=self.leaf,
                row=self.position.get_pos()[0]
            )
            return
        # Check the procedure has right amout of arguments
        if len(procedure.parameters) != len(self.children):
            self._logger.error_handler.add_error(
                2021,
                proc=self.leaf,
                row=self.position.get_pos()[0],
                args=len(self.children),
                params=len(procedure.parameters)
            )
        # Check procedure's arguments have right types
        for index, child in enumerate(self.children):
            child.check_types()
            if index >= len(procedure.parameters):
                continue
            argument_type = child.get_type()
            parameter_type = procedure.parameters[index].get_logotype()
            print(argument_type, type(argument_type), parameter_type, type(parameter_type))
            if argument_type != parameter_type:
                self._logger.error_handler.add_error(
                    2022,
                    proc=self.leaf,
                    arg=child.leaf,
                    atype=argument_type.value,
                    ptype=parameter_type.value,
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
        # Check the procedure hasn't already been declarated
        if self._symbol_tables.functions.lookup(self.leaf):
            self._logger.error_handler.add_error(2017, proc=self.leaf)
        self._symbol_tables.functions.insert(self.leaf, Function(self.leaf))
        procedure = self._symbol_tables.functions.lookup(self.leaf)
        self._symbol_tables.variables.initialize_scope(in_function=procedure)
        for child in self.children:
            child.check_types()

        # Check the procedure doesn't have unknown type parameters
        for parameter in procedure.parameters:
            if parameter.get_logotype() == LogoType.UNKNOWN:
                self._logger.error_handler.add_error(
                    2019,
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
        # Check the parameter hasn't already been declarated
        if self._symbol_tables.variables.lookup(self.leaf):
            self._logger.error_handler.add_error(2018, proc=procedure.name, param=self.leaf)
        variable = Variable(self.leaf)
        procedure.parameters.append(variable)
        self._symbol_tables.variables.insert(self.leaf, variable)
