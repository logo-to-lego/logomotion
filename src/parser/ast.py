# pylint: disable=missing-class-docstring,missing-function-docstring, unused-argument, too-many-instance-attributes
""" Abstract Syntax Tree node definitions, returned by the parser. """
from entities.logotypes import LogoType
from entities.symbol import Variable
from entities.symbol_tables import SymbolTables, default_symbol_tables
from lexer.token_types import TokenType
from utils.code_generator import default_code_generator
from utils.logger import Logger, default_logger


class Node:
    """Base AST Node class"""

    TEMP_VAR_INDEX = 0

    def __init__(self, node_type, children=None, leaf=None, **dependencies):
        self.type = node_type
        self.children = children if children else []
        self.leaf = leaf
        self._logger: Logger = dependencies.get("logger", default_logger)
        self._symbol_tables: SymbolTables = dependencies.get("symbol_tables", default_symbol_tables)
        self.position = dependencies.get("position", None)
        self._logo_type = None
        self._code_generator = dependencies.get("code_generator", default_code_generator)

    def get_type(self) -> LogoType:
        return self._logo_type

    def set_type(self, new_type: LogoType):
        self._logo_type = new_type

    def __str__(self):
        result = f"({self.type}"

        if self.leaf:
            result += f", {self.leaf if self.leaf else 'None'}"

        if self._logo_type:
            result += f", logo type: {self._logo_type.value}"

        if self.children:
            result += ", children: ["
            result += ", ".join((child.__str__() for child in self.children))
            result += "]"

        result += ")"

        return result

    def undefined_variables(self):
        """Checks if the current scope has undefined variables
        and returns a list of them.
        """
        undefined = []
        for symbol in self._symbol_tables.variables.get_current_scope().values():
            if symbol.type is LogoType.UNKNOWN:
                undefined.append(symbol.name)
        return undefined

    def generate_code(self):
        """Calls generate_code recursively on all child nodes."""
        for child in self.children:
            child.generate_code()

    def generate_temp_var(self):
        Node.TEMP_VAR_INDEX += 1
        return f"temp{Node.TEMP_VAR_INDEX}"


class Start(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("Start", children, **dependencies)

    def check_types(self):
        """Runs semantic analysis on the AST nodes to find type errors, undefined
        functions/variables and to figure out implied typing."""
        for child in self.children:
            child.check_types()


class StatementList(Node):
    def __init__(self, children=None, **dependencies):
        super().__init__("StatementList", children, None, **dependencies)

    def check_types(self):
        """Runs the check in given order."""
        for child in self.children:
            child.get_type()
            child.check_types()


class Move(Node):
    """FD, BK, LT, RT"""

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.VOID
        return self._logo_type

    def check_types(self):
        if len(self.children) != 1:
            self._logger.error_handler.add_error(
                2009, row=self.position.get_pos()[0], command=self.type.value
            )
            return

        child = self.children[0]
        child_type = child.get_type()
        if child_type == LogoType.UNKNOWN:
            child.set_type(LogoType.FLOAT)
        elif child_type != LogoType.FLOAT:
            self._logger.error_handler.add_error(
                2010,
                row=child.position.get_pos()[0],
                command=self.type.value,
                curr_type=child_type.value,
                expected_type=LogoType.FLOAT.value,
            )
        child.check_types()

    def generate_code(self):
        """Generate movement commands in Java."""
        arg_var = self.children[0].generate_code()

        if self.type == TokenType.FD:
            code = f"robot.travel({arg_var});"
        elif self.type == TokenType.BK:
            code = f"robot.travel(-{arg_var});"
        elif self.type == TokenType.LT:
            code = f"robot.rotate({arg_var});"
        # Else refers to rotate RT. This has to be changed
        # if other movement patterns are done.
        else:
            code = f"robot.rotate(-{arg_var});"

        self._logger.debug(code)
        self._code_generator.append_code(code)

class Make(Node):
    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.VOID
        return self._logo_type

    def check_types(self):
        # Check for right amount of params
        if len(self.children) != 1 or not self.leaf:
            self._logger.error_handler.add_error(
                2009, row=self.position.get_pos()[0], command=self.type.value
            )
            return

        # Check first argument type and variable name
        var_name = self.leaf
        var_name_type = var_name.get_type()

        if var_name_type == LogoType.UNKNOWN:
            var_name.set_type(LogoType.STRING)
        elif var_name.get_type() != LogoType.STRING:
            self._logger.error_handler.add_error(
                2010,
                row=self.position.get_pos()[0],
                command=self.type.value,
                curr_type=var_name.get_type().value,
                expected_type=LogoType.STRING.value,
            )
        var_name.check_types()

        # Check second argument type, assignment value
        value = self.children[0]
        value_type = value.get_type()

        if value_type == LogoType.VOID:
            self._logger.error_handler.add_error(
                2011,
                row=self.position.get_pos()[0],
                command=self.type.value,
                value_type=value_type.value,
            )
        value.check_types()

        # Check if var_name has symbol in symbol table
        symbol = self._symbol_tables.variables.lookup(var_name.leaf)
        if symbol:
            if symbol.type == LogoType.UNKNOWN:
                symbol.type = value.get_type()
            elif value.get_type() == LogoType.UNKNOWN:
                value.set_type(symbol.type)
            elif value.get_type() != symbol.type:
                self._logger.error_handler.add_error(
                    2012,
                    row=self.position.get_pos()[0],
                    var_name=var_name.leaf,
                    curr_type=symbol.type.value,
                    expected_type=value.get_type().value,
                )
        else:
            symbol = Variable(var_name.leaf, value.get_type())
            self._symbol_tables.variables.insert(var_name.leaf, symbol)


class Output(Node):
    def get_type(self):
        pass

    def check_types(self):
        pass


class Show(Node):
    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.VOID
        return self._logo_type

    def check_types(self):
        # Must have at least 1 param
        if len(self.children) == 0:
            self._logger.error_handler.add_error(2013, row=self.position.get_pos()[0])

        # Cannot be function call that returns VOID
        for child in self.children:
            logo_type = child.get_type()
            if logo_type == LogoType.VOID:
                self._logger.error_handler.add_error(
                    2014,
                    row=child.position.get_pos()[0],
                    command=self.type.value,
                    return_type=LogoType.VOID.value,
                )
            child.check_types()


class Bye(Node):
    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.VOID
        return self._logo_type

    def check_types(self):
        if self.children:
            self._logger.error_handler.add_error(2015, command=self.type.value)


class Command(Node):
    pass


class BinOp(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("BinOp", children, leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.FLOAT

        return self._logo_type

    def check_types(self):
        """Checks that the types of both operands is LogoFloat"""
        for child in self.children:
            child_type = child.get_type()
            if child_type == LogoType.UNKNOWN:
                child.set_type(LogoType.FLOAT)
            elif child_type != LogoType.FLOAT:
                self._logger.error_handler.add_error(2002, row=child.position.get_pos()[0])
            child.check_types()


class UnaryOp(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("UnaryOp", children, leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.FLOAT

        return self._logo_type

    def check_types(self):
        # Check UnaryOp type
        unary_type = self.get_type()
        if unary_type != LogoType.FLOAT:
            self._logger.error_handler.add_error(
                2003,
                row=self.position.get_pos()[0],
                curr_type=self._logo_type.value,
                expected_type=LogoType.FLOAT.value,
            )

        # Check the type of the child of UnaryOp
        for child in self.children:
            child_type = child.get_type()
            if child_type != LogoType.FLOAT:
                self._logger.error_handler.add_error(
                    2003,
                    row=child.position.get_pos()[0],
                    curr_type=child_type.value,
                    expected_type=LogoType.FLOAT.value,
                )


class RelOp(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("RelOp", children, leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.BOOL

        return self._logo_type

    def check_types(self):
        child1 = self.children[0]
        child2 = self.children[1]

        child1_type = child1.get_type()
        child2_type = child2.get_type()

        row = child1.position.get_pos()[0]

        if LogoType.UNKNOWN in (child1_type, child2_type):
            self._logger.error_handler.add_error(2004, row=row)

        if child1_type != child2_type:
            self._logger.error_handler.add_error(
                2005, row=row, type1=child1_type.value, type2=child2_type.value
            )


class Float(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Float", children=None, leaf=leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.FLOAT

        return self._logo_type

    def check_types(self):
        pass

    def generate_code(self):
        temp_var = self.generate_temp_var()
        code = f"double {temp_var} = {self.leaf};"
        self._logger.debug(code)
        self._code_generator.append_code(code)
        return temp_var


class Bool(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Bool", children=None, leaf=leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.BOOL

        return self._logo_type

    def check_types(self):
        pass


class Deref(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("Deref", children=None, leaf=leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.UNKNOWN

        symbol = self._get_symbol()

        if symbol:
            self._logo_type = symbol.typeclass

        return self._logo_type

    def set_type(self, new_type: LogoType):
        self._logo_type = new_type

        symbol = self._get_symbol()

        if symbol and symbol.typeclass == LogoType.UNKNOWN:
            symbol.typeclass = new_type

    def _get_symbol(self) -> Variable:
        return self._symbol_tables.variables.lookup(self.leaf)

    def check_types(self):
        symbol = self._get_symbol()
        if not symbol:
            self._logger.error_handler.add_error(2007, var=self.leaf)
        elif symbol.typeclass != self.get_type():
            self._logger.error_handler.add_error(
                2008,
                var=self.leaf,
                curr_type=symbol.typeclass.value,
                expected_type=self._logo_type.value,
            )


class StringLiteral(Node):
    def __init__(self, leaf, **dependencies):
        super().__init__("StringLiteral", children=None, leaf=leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.STRING

        return self._logo_type

    def check_types(self):
        pass


class If(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("If", children, leaf, **dependencies)

    def get_type(self):
        return None

    def check_types(self):
        if self.leaf.get_type() is not LogoType.BOOL:
            self._logger.error_handler.add_error(2006, row=self.position.get_pos()[0])
        self.leaf.check_types()
        self._symbol_tables.variables.initialize_scope()
        self.children[0].check_types()
        for variable in self.undefined_variables():
            self._logger.error_handler.add_error(2007, var=variable)
        self._symbol_tables.variables.finalize_scope()


class IfElse(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("IfElse", children, leaf, **dependencies)

    def get_type(self):
        return None

    def check_types(self):
        if self.leaf.get_type() is not LogoType.BOOL:
            self._logger.error_handler.add_error(2006, row=self.position.get_pos()[0])
        self.leaf.check_types()
        self._symbol_tables.variables.initialize_scope()
        for child in self.children:
            child.check_types()
        for variable in self.undefined_variables():
            self._logger.error_handler.add_error(2007, var=variable)
        self._symbol_tables.variables.finalize_scope()


class ProcDecl(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("ProcDecl", children, leaf, **dependencies)

    def get_type(self):
        if not self._logo_type:
            self._logo_type = LogoType.UNKNOWN

        return self._logo_type

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


class NodeFactory:
    """Used to create new AST nodes, injects logger and symbol table as dependencies."""

    def __init__(self, logger=default_logger,
            symbol_tables=default_symbol_tables,
            code_generator=default_code_generator
        ):

        self._logger = logger
        self._symbol_tables = symbol_tables
        self._code_generator = code_generator

    def create_node(self, node_class: Node, **kwargs):
        """Creates a new node of node_class, with the given keyword arguments."""
        return node_class(**kwargs, logger=self._logger,
               symbol_tables=self._symbol_tables,
               code_generator=self._code_generator)
