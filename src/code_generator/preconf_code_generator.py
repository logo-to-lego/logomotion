class JavaPreconfFuncsGenerator:
    """A class for generating preconfigured functions Java code
    """

    def __init__(self):
        pass

    def set_code_generator(self, jcg):
        # pylint: disable=W0201
        self.jcg = jcg

    def get_funcs(self):
        return {"repeat": self._repeat_code(),
                "for": self._for_code()}

    def _repeat_code(self):
        # pylint: disable=W0212
        mangled_name = self.jcg._mangle_java_function_name("repeat")
        java_repeat_code = f"public void {mangled_name}(DoubleVariable n, Runnable f) {{ \
                    for(int i=0;i<n.value;i++) {{ \
                        f.run();\
                    }} \
                  }}"
        return java_repeat_code

    def _for_code(self):
        # pylint: disable=W0212
        mangled_for = self.jcg._mangle_java_function_name("for")
        java_for_code = f"public void {mangled_for}(DoubleVariable itr, DoubleVariable start,\
            DoubleVariable limit, DoubleVariable step, Runnable f) {{\
                for (itr.value = start.value; itr.value <= limit.value; itr.value+=step.value) {{\
                    f.run();\
                }}\
            }}"
        return java_for_code