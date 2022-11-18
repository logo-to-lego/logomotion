class JavaPreconfFuncsGenerator:
    """A class for generating preconfigured functions Java code"""

    java_repeat_code = "public static void repeat(int n, Runnable f) {\
                    for(int i=0;i<n;i++) {\
                        f.run();\
                    }\
                  }"

    def __init__(self):
        self.java_preconf_funcs_dict = {"repeat": self.java_repeat_code}

    def get_funcs(self):
        return self.java_preconf_funcs_dict
