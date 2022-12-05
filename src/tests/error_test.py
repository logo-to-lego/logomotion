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
            "Kirjoitit 'mak'. En ymmärrä mitä tarkoitat."
        )
        eng_expected_msg = (
            "I could not understand 'mak'."
        )

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

        fin_expected_msg = "Sinä yritit tehdä laskutoimituksen jollakin joka ei ole numero."
        eng_expected_msg = "You tried to do a calculation with something that is not a number."

        self.assertEqual(len(self.error_handler.get_error_messages()), 1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg)

    def test_invalid_unary_op_with_bool(self):
        test_string = """
            make "a -false
            """

        ast = self.parser.parse(test_string)
        ast.check_types()

        fin_expected_msg = "Sinä kirjoitit, että tyyppi olisi 'BOOL', mutta se ei ole mahdollista. Tyypin pitää olla negatiivinen numero."
        eng_expected_msg = "You wrote that the type is 'BOOL', but that is impossible. Type should be a negative number"

        self.assertEqual(len(self.error_handler.get_error_messages()), 1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg)

    def test_invalid_unary_op_with_str(self):
        test_string = """
            make "a -"kissa
            """

        ast = self.parser.parse(test_string)
        ast.check_types()

        fin_expected_msg = "Sinä kirjoitit, että tyyppi olisi 'STRING', mutta se ei ole mahdollista. Tyypin pitää olla negatiivinen numero."
        eng_expected_msg = "You wrote that the type is 'STRING', but that is impossible. Type should be a negative number"

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

        fin_expected_msg1 = "Et ole määritellyt muuttujaa 'a'."
        eng_expected_msg1 = "You have not defined variable 'a'."
        fin_expected_msg2 = "Et ole määritellyt muuttujaa 'b'."
        eng_expected_msg2 = "You have not defined variable 'b'."

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

        fin_expected_msg = "Sinä yritit vertailla vääränlaisia tyyppejä keskenään. Vain numeroita ja merkkijonoja voi vertailla ja vertailtavien tyyppien pitää olla samat."
        eng_expected_msg = "You tried to compare wrong kind of types. Only numbers and strings can be compared and comparable types have to be the same kind of type."

        self.assertEqual(len(self.error_handler.get_error_messages()), 1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg)

    def test_variable_is_not_defined(self):
        test_string = """fd :x"""

        ast = self.parser.parse(test_string)
        ast.check_types()

        fin_expected_msg = "Et ole määritellyt muuttujaa 'x'."
        eng_expected_msg = "You have not defined variable 'x'."

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

        fin_expected_msg1 = "Sinä yritit antaa komennon FD parametrin tyypiksi STRING. Haluan, että parametri on tyyppi FLOAT."
        fin_expected_msg2 = "Sinä yritit antaa komennon BK parametrin tyypiksi BOOL. Haluan, että parametri on tyyppi FLOAT."
        fin_expected_msg3 = "Sinä yritit antaa komennon LT parametrin tyypiksi BOOL. Haluan, että parametri on tyyppi FLOAT."
        fin_expected_msg4 = "Sinä yritit antaa komennon RT parametrin tyypiksi STRING. Haluan, että parametri on tyyppi FLOAT."

        eng_expected_msg1 = "You tried to give STRING as the parameter's type for the command FD. I want the parameter type to be FLOAT."
        eng_expected_msg2 = "You tried to give BOOL as the parameter's type for the command BK. I want the parameter type to be FLOAT."
        eng_expected_msg3 = "You tried to give BOOL as the parameter's type for the command LT. I want the parameter type to be FLOAT."
        eng_expected_msg4 = "You tried to give STRING as the parameter's type for the command RT. I want the parameter type to be FLOAT."

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
        fin_expected_msg1 = "Sinä yritit antaa komennon MAKE parametrin tyypiksi BOOL. Haluan, että parametri on tyyppi STRING."
        fin_expected_msg2 = "Sinä yritit antaa komennon MAKE parametrin tyypiksi FLOAT. Haluan, että parametri on tyyppi STRING."

        eng_expected_msg1 = "You tried to give BOOL as the parameter's type for the command MAKE. I want the parameter type to be STRING."
        eng_expected_msg2 = "You tried to give FLOAT as the parameter's type for the command MAKE. I want the parameter type to be STRING."

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
            "Yritit muuttaa muuttujan 'a' tyyppiä tyypistä FLOAT tyyppiin STRING. En hyväksy tätä."
        )
        fin_expected_msg2 = (
            "Yritit muuttaa muuttujan 'a' tyyppiä tyypistä FLOAT tyyppiin BOOL. En hyväksy tätä."
        )

        eng_expected_msg1 = (
            "You tried to change variables a type from FLOAT to STRING. I don't like this."
        )
        eng_expected_msg2 = (
            "You tried to change variables a type from FLOAT to BOOL. I don't like this."
        )

        ast = self.parser.parse(test_string)
        ast.check_types()

        self.assertEqual(len(self.error_handler.get_error_messages()), 2)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg1)

        self.assertEqual(self.error_handler.get_error_messages()[1]["FIN"], fin_expected_msg2)
        self.assertEqual(self.error_handler.get_error_messages()[1]["ENG"], eng_expected_msg2)

    def test_make_raises_error_if_variable_name_is_deref(self):
        test_string = "make :muuttuja 42"

        fin_expected_msg1 = "Kirjoitit :muuttuja, tarkoititko \"muuttuja ?"
        eng_expected_msg1 = "You wrote :muuttuja, did you mean \"muuttuja ?"

        ast = self.parser.parse(test_string)
        ast.check_types()

        self.assertEqual(len(self.error_handler.get_error_messages()), 1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg1)

    def test_ifelse_raises_error_if_variable_referred_to_in_different_scope(self):
        test_string = "ifelse true {make \"test 10} {show :test}"

        fin_expected_msg1 = "Et ole määritellyt muuttujaa 'test'."
        eng_expected_msg1 = "You have not defined variable 'test'."

        ast = self.parser.parse(test_string)
        ast.check_types()

        self.assertEqual(len(self.error_handler.get_error_messages()), 1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["FIN"], fin_expected_msg1)
        self.assertEqual(self.error_handler.get_error_messages()[0]["ENG"], eng_expected_msg1)
