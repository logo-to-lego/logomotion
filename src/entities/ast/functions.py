# pylint disable=fixme
from entities.ast.node import Node
from entities.logotypes import LogoType
from entities.symbol import Function, Variable
from entities.type import Type
from entities.ast.variables import Deref
from utils.lowercase_converter import convert_to_lowercase as to_lowercase


class Output(Node):

    def get_logotype(self):
        return LogoType.VOID

    def check_types(self):
        self.children[0].check_types()
        output_value = self.children[0]
        procedure: Function = self._symbol_tables.variables.get_in_scope_function_symbol()
        # Check output command is in function
        if not procedure:
            self._logger.error_handler.add_error(
                2024, lexspan=self.position.get_lexspan(), row=self.position.get_pos()[0]
            )
            return
        if procedure.get_logotype() == LogoType.UNKNOWN:
            if output_value.__class__ == Deref:
                deref_symbol = self._symbol_tables.variables.lookup(output_value.leaf)
                if deref_symbol:
                    self._symbol_tables.concatenate_typeclasses(deref_symbol, procedure)
            else:
                procedure.typeclass.logotype = output_value.get_logotype()
        else:
            if output_value.get_logotype() == LogoType.UNKNOWN \
               and output_value.__class__ == Deref:
                deref_symbol = self._symbol_tables.variables.lookup(output_value.leaf)
                self._symbol_tables.concatenate_typeclasses(deref_symbol, procedure)
                return
            # Check output value's type is same as funtion's other output values' types
            if procedure.get_logotype() != output_value.get_logotype():
                self._logger.error_handler.add_error(
                    2025, lexspan=self.position.get_lexspan(), proc=procedure.name
                )

    def generate_code(self):
        output_var = self.children[0].generate_code()
        self._code_generator.return_statement(output_var)


class ProcCall(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("ProcCall", children, leaf, **dependencies)
        self.procedure: Function = None

    def get_logotype(self):
        proc = self.procedure if self.procedure else self._symbol_tables.functions.lookup(self.leaf)
        if proc:
            return proc.get_logotype()
        return None

    def get_typeclass(self):
        proc = self.procedure if self.procedure else self._symbol_tables.functions.lookup(self.leaf)
        if proc:
            return proc.typeclass
        return None

    def set_arguments_typeclass(self, argument, parameter):
        if argument.__class__ in (Deref, Function):
            arg_typeclass = argument.get_typeclass()
            arg_typeclass.logotype = parameter.get_logotype()

    def check_types(self):
        # Check the procedure has been declarated
        procedure = self._symbol_tables.functions.lookup(self.leaf)
        if not procedure:
            self._logger.error_handler.add_error(
                2020, self.position.get_lexspan(), proc=self.leaf, row=self.position.get_pos()[0]
            )
            return
        # Check the procedure has right amout of arguments
        if len(procedure.parameters) != len(self.children):
            self._logger.error_handler.add_error(
                2021,
                self.position.get_lexspan(),
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
            parameter_symbol = procedure.parameters[index]
            self.set_arguments_typeclass(child, parameter_symbol)
            argument_type = child.get_logotype()
            parameter_type = parameter_symbol.get_logotype()
            if argument_type != parameter_type:
                if parameter_type == LogoType.UNKNOWN:
                    self._logger.error_handler.add_error(
                        2026,
                        self.position.get_lexspan(),
                        proc=self.leaf,
                        atype=argument_type.value,
                    )
                else:
                    self._logger.error_handler.add_error(
                        2022,
                        self.position.get_lexspan(),
                        proc=self.leaf,
                        arg=child.leaf,
                        atype=argument_type.value,
                        ptype=parameter_type.value,
                        row=self.position.get_pos()[0],
                    )
        # Set the procedure as a parameter for use in code gen
        self.procedure = procedure

    def generate_code(self):
        temp_vars = []
        for child in self.children:
            temp_vars.append(child.generate_code())
        if self.get_logotype() == LogoType.VOID:
            self._code_generator.function_call(to_lowercase(self.leaf), temp_vars)
            return None
        return self._code_generator.returning_function_call(to_lowercase(self.leaf), temp_vars)


class ProcDecl(Node):
    def __init__(self, children, leaf, **dependencies):
        # Add this function as a defined function in the lexer.
        super().__init__("ProcDecl", children, leaf, **dependencies)
        self.procedure: Function = None

    def get_logotype(self):
        if self.procedure:
            return self.procedure.typeclass.logotype
        return None

    def check_types(self):
        # Check the procedure hasn't already been declarated
        if self._symbol_tables.functions.lookup(self.leaf):
            self._logger.error_handler.add_error(2017, self.position.get_lexspan(), proc=self.leaf)
        self.procedure = Function(self.leaf, typeclass=Type(functions={self.leaf}))
        self._symbol_tables.functions.insert(self.leaf, self.procedure)
        self._symbol_tables.variables.initialize_scope(in_function=self.procedure)
        for child in self.children:
            child.check_types()

        # Check the procedure doesn't have unknown type parameters
        for parameter in self.procedure.parameters:
            if parameter.get_logotype() == LogoType.UNKNOWN:
                self._logger.error_handler.add_error(
                    2019,
                    self.position.get_lexspan(),
                    proc=self.procedure.name,
                    param=parameter.name,
                )

        if (
            self.procedure.get_logotype() == LogoType.UNKNOWN
            and len(self.procedure.typeclass.variables) == 0
        ):
            self.procedure.typeclass.logotype = LogoType.VOID
        else:
            # Check function with output statements ends to output statement
            if not self.children[1].children[-1].__class__ == Output:
                self._logger.error_handler.add_error(
                    2027,
                    self.position.get_lexspan(),
                    proc=self.leaf
                )

        self._symbol_tables.variables.finalize_scope()

    def generate_code(self):
        self._code_generator.start_function_declaration(
            logo_func_name=to_lowercase(self.leaf), logo_func_type=self.get_logotype()
        )
        for child in self.children:
            child.generate_code()
        self._code_generator.end_function_declaration()


class ProcArgs(Node):
    def __init__(self, children, **dependencies):
        super().__init__("ProcArgs", children, **dependencies)

    def check_types(self):
        for child in self.children:
            child.check_types()

    def generate_code(self):
        parameters = []
        for child in self.children:
            parameters.append(child.get_param_data())
        self._code_generator.add_function_parameters(parameters=parameters)


class ProcArg(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("ProgArg", children, **dependencies)
        self.symbol: Variable = None

    def get_logotype(self):
        if self.symbol:
            return self.symbol.get_logotype()
        return None

    def check_types(self):
        procedure = self._symbol_tables.variables.get_in_scope_function_symbol()
        # Check the parameter hasn't already been declarated
        if self._symbol_tables.variables.lookup(self.leaf):
            self._logger.error_handler.add_error(
                2018, self.position.get_lexspan(), proc=procedure.name, param=self.leaf
            )
        self.symbol = Variable(self.leaf)
        procedure.parameters.append(self.symbol)
        self._symbol_tables.variables.insert(self.leaf, self.symbol)

    def get_param_data(self):
        """Return function parameter's type and name in tuple for ProgArgs' generate_code"""
        return (self.get_logotype(), to_lowercase(self.leaf))
