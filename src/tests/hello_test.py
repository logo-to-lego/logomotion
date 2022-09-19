import unittest
from hello import Hello
from unittest.mock import Mock


class TestHello(unittest.TestCase):
    """Test class for testing CI environment"""

    def setUp(self):
        self.mock = Mock()
        self.mock.hello_world.return_value = "hello world\n"

    def test_mock_prints_hello_world(self):
        Hello.hello_world(self.mock)
        self.assertEqual(self.mock.hello_world(), "hello world\n")
