import unittest

from mypy_pure.decorators import pure


class TestPureDecorators(unittest.TestCase):
    def test_pure_sets_attribute(self) -> None:
        @pure
        def add(a, b):
            return a + b

        self.assertTrue(getattr(add, '__pure__', False))
        self.assertEqual(add(2, 3), 5)
