import unittest

from importlib import import_module

import change_punct


class TestChangeNum(unittest.TestCase):

    def test_change(self):
        self.assertEqual('.PERIOD', change_punct.change_word('{.}'))
        self.assertEqual(',COMMA', change_punct.change_word('{,}'))
        self.assertEqual('?QUESTIONMARK', change_punct.change_word('{?}'))
        self.assertEqual('!EXCLAMATIONMARK', change_punct.change_word('{!}'))
        self.assertEqual(';SEMICOLON', change_punct.change_word('{;}'))
        self.assertEqual('-DASH', change_punct.change_word('{-}'))
        self.assertEqual(':COLON', change_punct.change_word('{:}'))

    def test_change_first(self):
            self.assertEqual('.PERIOD', change_punct.change_word('{.,:}'))
            self.assertEqual(',COMMA', change_punct.change_word('{ ",}'))

    def test_empty(self):
        self.assertEqual('', change_punct.change_word('{}'))
        self.assertEqual('', change_punct.change_word('{ "}'))

    def test_line(self):
        l, wc, pc = change_punct.change_line('vienas {,} du {.}')
        self.assertEqual('vienas ,COMMA du .PERIOD', l)
        self.assertEqual(4, wc)
        self.assertEqual(2, pc)


if __name__ == '__main__':
    unittest.main()
