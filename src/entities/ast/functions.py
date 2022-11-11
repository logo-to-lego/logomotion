# pylint disable=fixme
from entities.ast.node import Node
from entities.logotypes import LogoType
from entities.symbol import Function, Variable
from entities.type import Type
from entities.ast.variables import Deref


class Output(Node):
    def check_types(self):
        self.children[0].check_types()
        output_value = self.children[0]
        procedure: Function = self._symbol_tables.variables.get_in_scope_function_symbol()
        # Check output command is in function
        if not procedure:
            self._logger.error_handler.add_error(2024, row=self.position.get_pos()[0])
            return
        if procedure.get_logotype() == LogoType.UNKNOWN:
            if output_value.__class__ == Deref:
                deref_symbol = self._symbol_tables.variables.lookup(output_value.leaf)
                self._symbol_tables.concatenate_typeclasses(deref_symbol, procedure)
            else:
                procedure.typeclass.logotype = output_value.get_logotype()
        else:
            # Check output value's type is same as funtion's other output values' types
            if procedure.get_logotype() != output_value.get_logotype():
                self._logger.error_handler.add_error(2025, proc=procedure.name)

    def generate_code(self):
        pass


class ProcCall(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("ProcCall", children, leaf, **dependencies)

    def check_types(self):
        # Check the procedure has been declarated
        procedure = self._symbol_tables.functions.lookup(self.leaf)
        if not procedure:
            self._logger.error_handler.add_error(
                2020, proc=self.leaf, row=self.position.get_pos()[0]
            )
            return
        # Check the procedure has right amout of arguments
        if len(procedure.parameters) != len(self.children):
            self._logger.error_handler.add_error(
                2021,
                proc=self.leaf,
                row=self.position.get_pos()[0],
                args=len(self.children),
                params=len(procedure.parameters),
            )
        # Check procedure's arguments have right types
        for index, child in enumerate(self.children):
            child.check_types()
            if index >= len(procedure.parameters):
                break
            argument_type = child.get_logotype()
            parameter_type = procedure.parameters[index].get_logotype()
            if argument_type != parameter_type:
                self._logger.error_handler.add_error(
                    2022,
                    proc=self.leaf,
                    arg=child.leaf,
                    atype=argument_type.value,
                    ptype=parameter_type.value,
                    row=self.position.get_pos()[0],
                )

    def generate_code(self):
        pass


class ProcDecl(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("ProcDecl", children, leaf, **dependencies)

    def get_logotype(self):
        symbol = self._symbol_tables.functions.lookup(self.leaf)
        if symbol:
            return symbol.typeclass.logotype
        return None

    def check_types(self):
        # Check the procedure hasn't already been declarated
        if self._symbol_tables.functions.lookup(self.leaf):
            self._logger.error_handler.add_error(2017, proc=self.leaf)
        procedure = Function(self.leaf, typeclass=Type(functions={self.leaf}))
        self._symbol_tables.functions.insert(self.leaf, procedure)
        self._symbol_tables.variables.initialize_scope(in_function=procedure)
        for child in self.children:
            child.check_types()

        # Check the procedure doesn't have unknown type parameters
        for parameter in procedure.parameters:
            if parameter.get_logotype() == LogoType.UNKNOWN:
                self._logger.error_handler.add_error(
                    2019, proc=procedure.name, param=parameter.name
                )

        if procedure.get_logotype() == LogoType.UNKNOWN and len(procedure.typeclass.variables) == 0:
            procedure.typeclass.logotype = LogoType.VOID

        self._symbol_tables.variables.finalize_scope()

    def generate_code(self):
        pass
        # määritä funktio code_genissä: "public {tyyppi=get_logotype()} {nimi=self.leaf} (..."
        # self.children[0].generate_code()
        # code_gen: "...) {..."
        # self.children[1].generate_code()
        # code_gen: "...}"

class ProcArgs(Node):
    def __init__(self, children, **dependencies):
        super().__init__("ProcArgs", children, **dependencies)

    def check_types(self):
        for child in self.children:
            child.check_types()

    def generate_code(self):
        pass
        # for child in self.childrens:
        #    child.generate_code()


class ProcArg(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("ProgArg", children, **dependencies)
        self.symbol: Variable = None

    def get_logotype(self):
        return self._symbol_tables.variables.lookup(self.leaf)

    def check_types(self):
        procedure = self._symbol_tables.variables.get_in_scope_function_symbol()
        # Check the parameter hasn't already been declarated
        if self._symbol_tables.variables.lookup(self.leaf):
            self._logger.error_handler.add_error(2018, proc=procedure.name, param=self.leaf)
        self.symbol = Variable(self.leaf)
        procedure.parameters.append(self.symbol)
        self._symbol_tables.variables.insert(self.leaf, self.symbol)

    def generate_code(self):
        pass
        # code_gen: määritetään parametrin nimi ja tyyppi
