from entities.ast.functions import ProcCall
from entities.ast.node import Node
from entities.ast.variables import Deref
from entities.logotypes import LogoType


class BinOp(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("BinOp", children, leaf, **dependencies)

    def get_logotype(self):
        return LogoType.FLOAT

    def check_types(self):
        """Checks that the types of both operands is LogoFloat"""
        for child in self.children:
            child.check_types()

            if child.__class__ == Deref and child.get_logotype() == LogoType.UNKNOWN:
                child.set_logotype(LogoType.FLOAT)

            if child.__class__ == ProcCall and child.get_logotype() == LogoType.UNKNOWN:
                child.set_logotype(LogoType.FLOAT)

            if child.get_logotype() != LogoType.FLOAT:
                self._logger.error_handler.add_error(
                    2002, self.position.get_lexspan(), row=child.position.get_pos()[0]
                )

    def generate_code(self):
        """Generate binop to java"""
        arg_var1 = self.children[0].generate_code()
        arg_var2 = self.children[1].generate_code()
        return self._code_generator.binop(arg_var1, arg_var2, self.leaf)


class UnaryOp(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("UnaryOp", children, leaf, **dependencies)

    def get_logotype(self):
        return LogoType.FLOAT

    def check_types(self):
        # Check UnaryOp type
        unary_type = self.get_logotype()
        if unary_type != LogoType.FLOAT:
            self._logger.error_handler.add_error(
                2003,
                self.position.get_lexspan(),
                row=self.position.get_pos()[0],
                curr_type=self.get_logotype().value,  # _logo_type.value,
                expected_type=LogoType.FLOAT.value,
            )

        # Check the type of the child of UnaryOp
        for child in self.children:
            child_type = child.get_logotype()
            if child_type != LogoType.FLOAT:
                self._logger.error_handler.add_error(
                    2003,
                    self.position.get_lexspan(),
                    row=child.position.get_pos()[0],
                    curr_type=child_type.value,
                    expected_type=LogoType.FLOAT.value,
                )

    def generate_code(self):
        arg_var = self.children[0].generate_code()
        return self._code_generator.unary_op(arg_var)


class RelOp(Node):
    def __init__(self, children, leaf, **dependencies):
        super().__init__("RelOp", children, leaf, **dependencies)

    def get_logotype(self):
        return LogoType.BOOL

    def check_types(self):
        child1 = self.children[0]
        child2 = self.children[1]

        child1.check_types()
        child2.check_types()

        row = child1.position.get_pos()[0]

        allowed_types = [LogoType.UNKNOWN, LogoType.FLOAT, LogoType.STRING]

        # Deref.get_logotype() returns None if variable is not defined
        if child1.get_logotype() is None or child2.get_logotype() is None:
            return

        # Check that given types are comparable
        if child1.get_logotype() not in allowed_types or child2.get_logotype() not in allowed_types:
            self._logger.error_handler.add_error(
                2005,
                self.position.get_lexspan(),
                row=row,
                type1=child1.get_logotype().value,
                type2=child2.get_logotype().value,
            )
            return

        # Types can be different only if at least one of them is unknown
        if child1.get_logotype() == LogoType.UNKNOWN:
            child1.set_logotype(child2.get_logotype())
        elif child2.get_logotype() == LogoType.UNKNOWN:
            child2.set_logotype(child1.get_logotype())

        # If after setting unknown types the types are still not the same -> error
        if child1.get_logotype() != child2.get_logotype():
            self._logger.error_handler.add_error(
                2005,
                self.position.get_lexspan(),
                row=row,
                type1=child1.get_logotype().value,
                type2=child2.get_logotype().value,
            )
            return

        # Equals (=) and not equals (<>) can be used with FLOAT AND STRING
        if self.leaf in ("<>", "="):
            # If type could not be inferred -> error
            if (
                child1.get_logotype() == LogoType.UNKNOWN
                and child2.get_logotype() == LogoType.UNKNOWN
            ):
                self._logger.error_handler.add_error(2004, self.position.get_lexspan(), row=row)
                return

        # <, >, <= and >= can only be used with type FLOAT
        elif self.leaf in ("<", ">", "<=", ">="):
            if child1.get_logotype() == LogoType.UNKNOWN:
                child1.set_logotype(LogoType.FLOAT)
            if child2.get_logotype() == LogoType.UNKNOWN:
                child2.set_logotype(LogoType.FLOAT)

            if (
                child1.get_logotype() is not LogoType.FLOAT
                or child2.get_logotype() is not LogoType.FLOAT
            ):
                self._logger.error_handler.add_error(
                    2016,
                    self.position.get_lexspan(),
                    row=row,
                    type1=child1.get_logotype().value,
                    type2=child2.get_logotype().value,
                )

    def generate_code(self):
        """Generate relop to java"""
        arg_var1 = self.children[0].generate_code()
        arg_var2 = self.children[1].generate_code()

        return self._code_generator.relop(arg_var1, arg_var2, self.leaf)
