class JavaPreconfFuncsGenerator:
    """A class for generating preconfigured functions Java code"""

    java_repeat_code = "public static void repeat(int n, Runnable f) {\
                    for(int i=0;i<n;i++) {\
                        f.run();\
                    }\
                  }"
                  
    java_for_code = "public static void repeat(String varname, int itr, int limit, Runnable f) {\
        for(int varname=itr;limit<=itr;itr++) {\
            f.run();\
            }}\
            \
            public static void repeat(String varname, int itr, int limit, int stepsize, Runnable f) {\
                for(int varname = itr ; itr <= limit ; itr += stepsize) {\
                    f.run()\
                    }}"
                  
    #Typical for loop. The controllist specifies three or four members: 
    # the local varname, start value, limit value, and optional step size

    def __init__(self):
        self.java_preconf_funcs_dict = {"repeat": self.java_repeat_code}

    def get_funcs(self):
        return self.java_preconf_funcs_dict
