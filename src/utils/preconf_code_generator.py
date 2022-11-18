class JavaPreconfFuncsGenerator:
    """A class for generating preconfigured functions Java code"""
    
    def __init__(self):
        self.java_preconf_funcs_dict = {"repeat": self.get_repeat_java()}
    
    def get_repeat_java(self):
        repeat_code = "public static void repeat(int n, Runnable f) { \
                    for(int i=0;i<2;i++) { \
                        f.run(); \
                    } \
                  }"
        return repeat_code
    
    def get_funcs(self):
        return self.java_preconf_funcs_dict
    

        