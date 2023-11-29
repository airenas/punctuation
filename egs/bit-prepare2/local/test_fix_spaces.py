import unittest

from importlib import import_module

import fix_spaces


class TestChangeLine(unittest.TestCase):

    def test_add_space(self):
        self.assertEqual(fix_spaces.change_line('olia{.}'), 'olia {.}')

    def test_add_space2(self):
        self.assertEqual(fix_spaces.change_line('olia{.}aa'), 'olia {.} aa')
        self.assertEqual(fix_spaces.change_line('{x}olia{.}aa'), '{x} olia {.} aa')

    def test_drop_inside(self):
        self.assertEqual(fix_spaces.change_line('olia{. ,}aa, a.'), 'olia {.,} aa, a.')
        self.assertEqual(fix_spaces.change_line('olia{. ,}aa, {   }a.'), 'olia {.,} aa, {} a.')

    def test_fails(self):
        with self.assertRaises(AssertionError):
            fix_spaces.change_line('olia{{. ,}aa, a.')
        with self.assertRaises(AssertionError):
            fix_spaces.change_line('olia{. ,}}aa, a.')


if __name__ == '__main__':
    unittest.main()

