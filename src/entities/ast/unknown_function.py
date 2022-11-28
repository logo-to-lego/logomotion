from entities.ast.node import Node
from entities.logotypes import LogoType
from entities.symbol import Variable, Function
from entities.type import Type


class UnknownFunction(Node):
    """Todo:
        Tän pitäis saada tietää for looppia kutsuttaessa for:in argumenteista
        2 ekaa eli esim kutsulla for ["wasd 3 2 1] {tää} pitäis saada tietää
        "wasd ja 3 jolloin näistä muodostetaan oma variaabeli
        jonka jälkeen aloitetaan oma funktioskope
    Args:
        arg_type: either a LogoType or False.
        param_specs: for loop iter information passed from proccall
    """
    def __init__(self, children=None, **dependencies):
        super().__init__("UnknownFunction", children, None, **dependencies)
        self._arg_type = dependencies.get("arg_type", False)
        pos_iter_param = dependencies.get("iter_param", None)
        if pos_iter_param:
            self._iter_param = pos_iter_param.leaf
        else:
            self._iter_param = None


    def get_logotype(self) -> LogoType:
        return LogoType.NAMELESS_FUNCTION

    def check_types(self):
        """Creates a variable to scope
        if given code is `for ["a 1 2 3] {...}` creates variable 'a'
        """
        # pass 'fake' Function instance to symbol table, so it'll create a local scope
        self.procedure = Function("for", typeclass=Type(functions={"for"}))
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
