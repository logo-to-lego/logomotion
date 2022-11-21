class JavaPreconfFuncsGenerator:
    """A class for generating preconfigured functions Java code
    
    TODO 
    koodi generoituu logo.func1(temp18, temp19) -> miksi 'logo.funktio'
    """
    
    """ java_repeat_code = "public void repeat(double n, Runnable f) {\
                    for(int i=0;i<n;i++) {\
                        f.run();\
                    }\
                  }"
                  
    java_for_code = "public void logo_for(double itr, double start, double limit, Runnable f) {\
        for(itr=start;itr<=limit;itr++) {\
            f.run();\
            }}\
            \
            public void logo_for(double itr, double start, double limit, double step, Runnable f) {\
                for (itr = start; itr <= limit; itr+=step) {\
                    f.run();\
                }\
            }"
     """
    def __init__(self):
        pass

    def give_code_generator(self, jcg):
        self.jcg = jcg
    
    def get_funcs(self):
        return {"repeat": self._repeat_code(),
                "for": self._for_code()}

    def _repeat_code(self):
        mangled_name = self.jcg._mangle_java_function_name("repeat")
        java_repeat_code = f"public static void {mangled_name}(double n, Runnable f) {{ \
                    for(int i=0;i<n;i++) {{ \
                        f.run();\
                    }} \
                  }}"
        return java_repeat_code
    
    def _for_code(self):
        #itr -> variable taulusta
        mangled_for = self.jcg._mangle_java_function_name("for")
        java_for_code = f"public void {mangled_for}(double itr, double start, double limit, Runnable f) {{\
        for(itr=start;itr<=limit;itr++) {{\
            f.run();\
            }}\
            }}\
            \
            public void {mangled_for}(double itr, double start, double limit, double step, Runnable f) {{\
                for (itr = start; itr <= limit; itr+=step) {{\
                    f.run();\
                }}\
            }}"
        return java_for_code