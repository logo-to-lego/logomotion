class JavaPreconfFuncsGenerator:
    """A class for generating preconfigured functions Java code
    TODO
    koodi generoituu logo.func1(temp18, temp19) -> miksi 'logo.funktio'
    """

    def __init__(self):
        pass

    def give_code_generator(self, jcg):
        # pylint: disable=W0201
        self.jcg = jcg

    def get_funcs(self):
        return {"repeat": self._repeat_code(),
                "for": self._for_code()}

    def _repeat_code(self):
        # pylint: disable=W0212
        mangled_name = self.jcg._mangle_java_function_name("repeat")
        java_repeat_code = f"public static void {mangled_name}(double n, Runnable f) {{ \
                    for(int i=0;i<n;i++) {{ \
                        f.run();\
                    }} \
                  }}"
        return java_repeat_code

    def _for_code(self):
        # pylint: disable=W0212
        mangled_for = self.jcg._mangle_java_function_name("for")
        java_for_code = f"public void {mangled_for}(String placeholder, double start, \
            double limit, Consumer<Variable> f) {{\
        Variable new_var = new Variable(0); \
        for(double itr=start;itr<=limit;itr++) {{\
            new_var.value = itr;\
            f.accept(new_var);\
            }}\
            }}\
            \
            public void {mangled_for}(String placeholder, double start, double limit, double step, Consumer<Variable> f) {{\
                Variable new_var = new Variable(0); \
                for (double itr = start; itr <= limit; itr+=step) {{\
                    new_var.value = itr;\
                    f.accept(new_var);\
                }}\
            }}"
        return java_for_code
