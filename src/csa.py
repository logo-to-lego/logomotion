"""Analysis module
Check function and variable variable existence & values from symbol tables when called 
"""


def binop_eval(binop):
    """
    Existence at current scope
    Typecheck vis a vis operator
    """
    print("----")
    print(binop)  # [x for x in fruits if "a" in x]
    if "Deref" in [child.type for child in binop.children]:
        print("Deref in children")
    # for child in binop.children:
    #    print(child.type)


mdict = {"BinOp": binop_eval}


def evals(arg):
    print("printed from csa_eval")
    f = mdict[arg.type]
    f(arg)
