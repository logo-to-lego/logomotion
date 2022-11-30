from entities.ast.node import Node
from entities.logotypes import LogoType
from entities.symbol import Variable, Function
from entities.type import Type


class UnknownFunction(Node):
    """
    Args:
        arg_type: either a LogoType or False.
        param_specs: for loop iter information passed from proccall
    """
    def __init__(self, children=None, **dependencies):
        super().__init__("UnknownFunction", children, None, **dependencies)
        iter = dependencies.get("iter_param", None)
        self._iter_param = iter.leaf if iter else None

    def get_logotype(self) -> LogoType:
        return LogoType.NAMELESS_FUNCTION

    def check_types(self):
        self._symbol_tables.variables.initialize_scope()
        # if we're handling a for loop, we need to add the iterator to the scope
        if self._iter_param:
            symbol = Variable(self._iter_param, Type(LogoType.FLOAT, variables={self._iter_param}))
            self._symbol_tables.variables.insert(self._iter_param, symbol)
        for child in self.children:
            child.check_types()
        self._symbol_tables.variables.finalize_scope()

    def generate_code(self):
        """Generate block into for or repeat lambda-statement"""
        if self._iter_param:
            tmpvar = self._code_generator.lambda_param_start(self._iter_param)
        else:
            tmpvar = self._code_generator.lambda_no_param_start()
        for child in self.children:
            child.generate_code()
        self._code_generator.lambda_end()
        return tmpvar
