# pylint: disable=missing-module-docstring, too-few-public-methods
class Hello:
    """Test class for testing CI environment"""

    @staticmethod
    def hello_world(console_io):
        """Hello world

        Args:
            console_io (IO objeck): object (mock) for IO operations
        """
        console_io.write("hello world")
