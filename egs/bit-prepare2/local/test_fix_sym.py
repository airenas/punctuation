import unittest

from importlib import import_module

import fix_sym


class TestChangeNum(unittest.TestCase):

    def test_no_change(self):
        self.assertEqual('- žmonėms patinka{-}taip', fix_sym.change_line('- žmonėms patinka{-}taip'))

    def test_change(self):
        self.assertEqual('žmonėms patinka{-}taip', fix_sym.change_line('žmonėms patinka{–}taip'))


if __name__ == '__main__':
    unittest.main()
