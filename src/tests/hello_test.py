import unittest
from unittest.mock import Mock

class TestHello(unittest.TestCase):
    """Test class for testing CI environment
    """

    def setUp(self):
        self.mock = Mock()
        self.mock.hello.return_value = "hello world\n"

    def test_mock_prints_hello_world(self):
        self.assertEqual(self.mock.hello(), "hello world\n")
