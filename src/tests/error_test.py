import unittest
from unittest.mock import Mock
from lexer.lexer import Lexer
from parser.parser import Parser
from utils.error_handler import ErrorHandler
from utils.logger import Logger
from entities.symbol_tables import SymbolTables
from entities.symbol_table import SymbolTable


class TestErrorHandler(unittest.TestCase):
    """Test class for testing error handler"""

    def setUp(self):
        self.console_mock = Mock()
        self.error_handler = ErrorHandler(console_io=self.console_mock)
        self.logger = Logger(self.console_mock, self.error_handler)
        self.lexer = Lexer(self.logger)
        self.lexer.build()
        self.symbol_tables = SymbolTables(SymbolTable(), SymbolTable())

        self.parser = Parser(self.lexer, self.logger, self.symbol_tables)
        self.parser.build()

    def test_valid_logo_code_does_not_yield_errors(self):
        test_string = """
            make "a 123
            show :a
            make "b true
        """

        ast = self.parser.parse(test_string)
        ast.check_types()

        self.assertEqual(len(self.error_handler.get_error_messages()), 0)

    def test_error_with_invalid_make_keyword(self):
        test_string = """mak "asd 123"""

        self.parser.parse(test_string)
        fin_expected_msg = (
            "En saanut selvää komennosta 'mak'. Löysin tämän riviltä 1 ja sarakkeelta 3."
        )
        eng_expected_msg = "I could not understand 'mak'. I found this on row 1 and column 3."

        self.assertEqual(len(self.error_handler.get_error_messages()), 1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg)

    def test_error_with_invalid_binop(self):
        test_string = """
            make "a "kissa
            make "b 1 + :a
            """

        ast = self.parser.parse(test_string)
        ast.check_types()

        fin_expected_msg = "Rivillä 3 yritit tehdä laskutoimituksen jollakin joka ei ole numero."
        eng_expected_msg = "In row 3 you tried to calculate with something that is not a number."

        self.assertEqual(len(self.error_handler.get_error_messages()), 1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg)

    def test_invalid_unary_op_with_bool(self):
        test_string = """
            make "a -false
            """

        ast = self.parser.parse(test_string)
        ast.check_types()

        fin_expected_msg = (
            "Rivillä 2 negatiivisen luvun tyyppi on BOOL, vaikka sen pitäisi olla FLOAT."
        )
        eng_expected_msg = (
            "In row 2 the type of a negative number is BOOL, even though it should be FLOAT."
        )

        self.assertEqual(len(self.error_handler.get_error_messages()), 1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg)

    def test_invalid_unary_op_with_str(self):
        test_string = """
            make "a -"kissa
            """

        ast = self.parser.parse(test_string)
        ast.check_types()

        fin_expected_msg = (
            "Rivillä 2 negatiivisen luvun tyyppi on STRING, vaikka sen pitäisi olla FLOAT."
        )
        eng_expected_msg = (
            "In row 2 the type of a negative number is STRING, even though it should be FLOAT."
        )

        self.assertEqual(len(self.error_handler.get_error_messages()), 1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg)

    def test_valid_relops_work(self):
        test_string = """
            make "a "kissa
            make "b 42
            make "c :a <> "koira
            make "d :b > 100
        """

        ast = self.parser.parse(test_string)
        ast.check_types()

        self.assertEqual(len(self.error_handler.get_error_messages()), 0)

    def test_relop_raises_error_with_undefined_variables(self):
        test_string = """make "c :a >= :b"""

        ast = self.parser.parse(test_string)
        ast.check_types()

        fin_expected_msg1 = "Muuttujaa 'a' ei ole määritelty."
        eng_expected_msg1 = "Variable 'a' is not defined."
        fin_expected_msg2 = "Muuttujaa 'b' ei ole määritelty."
        eng_expected_msg2 = "Variable 'b' is not defined."

        self.assertEqual(len(self.error_handler.get_error_messages()), 2)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg1)
        self.assertEqual(self.error_handler.get_error_messages()[1]["FIN"], fin_expected_msg2)
        self.assertEqual(self.error_handler.get_error_messages()[1]["ENG"], eng_expected_msg2)

    def test_relop_raises_error_with_non_comparable_types(self):
        test_string = """
            make "a "abc
            make "b 123
            make "c :a >= :b
            """

        ast = self.parser.parse(test_string)
        ast.check_types()

        fin_expected_msg = "Rivillä 4 koitit vertailla tyyppejä STRING ja FLOAT. Katso, että tyypit ovat joko FLOAT tai STRING tyyppisiä ja keskenään samat"
        eng_expected_msg = "In row 4 you tried to compare types STRING and FLOAT. Check that you are comparing FLOAT or STRING types and that the types are equal"

        self.assertEqual(len(self.error_handler.get_error_messages()), 1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg)

    def test_variable_is_not_defined(self):
        test_string = """fd :x"""

        ast = self.parser.parse(test_string)
        ast.check_types()

        fin_expected_msg = "Muuttujaa 'x' ei ole määritelty."
        eng_expected_msg = "Variable 'x' is not defined."

        self.assertEqual(len(self.error_handler.get_error_messages()), 1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg)

    def test_move_commands_yield_error_with_invalid_parameter_type(self):
        test_string = """
            make "a "somevalue
            fd "abc
            bk true
            lt false
            rt :a
            """

        fin_expected_msg1 = (
            "Rivillä 3 komennon 'FD' parametri on tyyppiä STRING, vaikka sen pitäisi olla FLOAT."
        )
        fin_expected_msg2 = (
            "Rivillä 4 komennon 'BK' parametri on tyyppiä BOOL, vaikka sen pitäisi olla FLOAT."
        )
        fin_expected_msg3 = (
            "Rivillä 5 komennon 'LT' parametri on tyyppiä BOOL, vaikka sen pitäisi olla FLOAT."
        )
        fin_expected_msg4 = (
            "Rivillä 6 komennon 'RT' parametri on tyyppiä STRING, vaikka sen pitäisi olla FLOAT."
        )

        eng_expected_msg1 = (
            "In row 3 the parameter of 'FD' was type STRING, even though it should be FLOAT."
        )
        eng_expected_msg2 = (
            "In row 4 the parameter of 'BK' was type BOOL, even though it should be FLOAT."
        )
        eng_expected_msg3 = (
            "In row 5 the parameter of 'LT' was type BOOL, even though it should be FLOAT."
        )
        eng_expected_msg4 = (
            "In row 6 the parameter of 'RT' was type STRING, even though it should be FLOAT."
        )

        ast = self.parser.parse(test_string)
        ast.check_types()

        self.assertEqual(len(self.error_handler.get_error_messages()), 4)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg1)

        self.assertEqual(self.error_handler.get_error_messages()[1]["FIN"], fin_expected_msg2)
        self.assertEqual(self.error_handler.get_error_messages()[1]["ENG"], eng_expected_msg2)

        self.assertEqual(self.error_handler.get_error_messages()[2]["FIN"], fin_expected_msg3)
        self.assertEqual(self.error_handler.get_error_messages()[2]["ENG"], eng_expected_msg3)

        self.assertEqual(self.error_handler.get_error_messages()[3]["FIN"], fin_expected_msg4)
        self.assertEqual(self.error_handler.get_error_messages()[3]["ENG"], eng_expected_msg4)

    def test_make_only_accepts_string_as_variable_name(self):
        test_string = """
            make true "abc
            make 123 456
            make "foo "bar
        """
        fin_expected_msg1 = (
            "Rivillä 2 komennon 'MAKE' parametri on tyyppiä BOOL, vaikka sen pitäisi olla STRING."
        )
        fin_expected_msg2 = (
            "Rivillä 3 komennon 'MAKE' parametri on tyyppiä FLOAT, vaikka sen pitäisi olla STRING."
        )

        eng_expected_msg1 = (
            "In row 2 the parameter of 'MAKE' was type BOOL, even though it should be STRING."
        )
        eng_expected_msg2 = (
            "In row 3 the parameter of 'MAKE' was type FLOAT, even though it should be STRING."
        )

        ast = self.parser.parse(test_string)
        ast.check_types()

        self.assertEqual(len(self.error_handler.get_error_messages()), 2)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg1)

        self.assertEqual(self.error_handler.get_error_messages()[1]["FIN"], fin_expected_msg2)
        self.assertEqual(self.error_handler.get_error_messages()[1]["ENG"], eng_expected_msg2)

    def test_make_only_accepts_same_type_as_new_value(self):
        test_string = """
            make "a 123
            make "a "abc
            make "a true
            make "a 456
        """
        fin_expected_msg1 = (
            "Rivillä 3 muuttujan 'a' tyyppiä ei voi vaihtaa tyypistä FLOAT tyyppiin STRING."
        )
        fin_expected_msg2 = (
            "Rivillä 4 muuttujan 'a' tyyppiä ei voi vaihtaa tyypistä FLOAT tyyppiin BOOL."
        )

        eng_expected_msg1 = (
            "In row 3 variable 'a' has type FLOAT which cannot be changed to type STRING."
        )
        eng_expected_msg2 = (
            "In row 4 variable 'a' has type FLOAT which cannot be changed to type BOOL."
        )

        ast = self.parser.parse(test_string)
        ast.check_types()

        self.assertEqual(len(self.error_handler.get_error_messages()), 2)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg1)

        self.assertEqual(self.error_handler.get_error_messages()[1]["FIN"], fin_expected_msg2)
        self.assertEqual(self.error_handler.get_error_messages()[1]["ENG"], eng_expected_msg2)
