from entities.ast.node import Node
from entities.logotypes import LogoType


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

    def generate_code(self):
        """Generate binop to java"""
        arg_var1 = self.children[0].generate_code()
        arg_var2 = self.children[1].generate_code()
        return self._code_generator.binop(arg_var1, arg_var2, self.leaf)


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

        child1.check_types()
        child2.check_types()

        child1_type = child1.get_type()
        child2_type = child2.get_type()

        row = child1.position.get_pos()[0]

        if LogoType.UNKNOWN in (child1_type, child2_type):
            self._logger.error_handler.add_error(2004, row=row)

        if child1_type != child2_type:
            self._logger.error_handler.add_error(
                2005, row=row, type1=child1_type.value, type2=child2_type.value
            )
