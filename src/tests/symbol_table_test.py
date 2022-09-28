import unittest
from entities.symbol_table import SymbolTable


class TestSymbolTable(unittest.TestCase):
    """test class for entities.symbol_table.SymbolTable"""

    def setUp(self):
        self.st = SymbolTable()
        self.value1 = 123
        self.value2 = 456

    def test_inserted_reference_is_found(self):
        self.st.insert("x", self.value1)
        re = self.st.lookup("x")
        self.assertEqual(self.value1, re)

    def test_insertion_is_found_after_changing_the_scope(self):
        self.st.insert("x", self.value1)
        self.st.initialize_scope()
        re = self.st.lookup("x")
        self.assertEqual(self.value1, re)

    def test_insertion_can_be_overwriten_in_upper_level_scope(self):
        self.st.insert("x", self.value1)
        self.st.initialize_scope()
        self.st.insert("x", self.value2)
        re = self.st.lookup("x")
        self.assertEqual(self.value2, re)

    def test_lower_level_scope_insertion_remains_after_upper_level_changes(self):
        self.st.insert("x", self.value1)
        self.st.initialize_scope()
        self.st.insert("x", self.value2)
        self.st.finalize_scope()
        re = self.st.lookup("x")
        self.assertEqual(self.value1, re)

    def test_lookup_returns_none_if_insertion_doesnt_exist(self):
        self.st.insert("x", self.value1)
        re = self.st.lookup("y")
        self.assertEqual(None, re)

    def test_current_level_insertions_are_erased_after_free(self):
        self.st.insert("x", self.value1)
        self.st.initialize_scope()
        self.st.insert("x", self.value2)
        re1 = self.st.lookup("x")
        self.st.free()
        re2 = self.st.lookup("x")
        self.assertEqual(self.value2, re1)
        self.assertEqual(self.value1, re2)

    def test_finalize_scope_cant_be_run_on_lowest_scope_level(self):
        self.st.initialize_scope()
        re1 = self.st.finalize_scope()
        re2 = self.st.finalize_scope()
        self.assertEqual(True, re1)
        self.assertEqual(False, re2)

    def test_insert_global_inserts_symbol_to_global_scope(self):
            self.st.initialize_scope()
            self.st.insert_global("x", self.value1)
            self.st.insert("x", self.value2)
            self.st.initialize_scope()
            self.st.insert_global("y", self.value2)
            re_local = self.st.lookup("x")
            self.st.finalize_scope()
            self.st.finalize_scope()
            re_global1 = self.st.lookup("x")
            re_global2 = self.st.lookup("y")
            self.assertEqual(re_local, self.value2)
            self.assertEqual(re_global1, self.value1)
            self.assertEqual(re_global2, self.value2)
