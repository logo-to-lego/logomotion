"""Code Generator module"""

START = "public class Logomotion { public static void main(string[] args) { "
END = " } }"
DEFAULT_NAME = "logomotion"

class CodeGenerator:
    """A class for generating code"""

    def __init__(self, name=DEFAULT_NAME):
        self._code = []
        self._name = name

    def append_code(self, line: str):
        """append code line to generator"""
        self._code.append(line)

    def write(self):
        """write Java file"""
        with open(self._name + ".java", mode="w", encoding="utf-8") as writer:
            writer.write(START)
            for line in self._code:
                writer.write(line + " ")
            writer.write(END)

default_code_generator = CodeGenerator()
