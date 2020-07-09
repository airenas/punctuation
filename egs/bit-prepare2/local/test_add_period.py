import io
import unittest

import add_period


class TestJoinSentence(unittest.TestCase):

    def test_leave(self):
        f_in = io.StringIO("a ?QUESTIONMARK\nb .PERIOD\n")
        f_out = io.StringIO()
        add_period.process(f_in, f_out)
        f_out.seek(0)
        l = f_out.read()
        self.assertEqual('a ?QUESTIONMARK\nb .PERIOD\n', l)

    def test_changes(self):
        f_in = io.StringIO("a\nb\n")
        f_out = io.StringIO()
        add_period.process(f_in, f_out)
        f_out.seek(0)
        l = f_out.read()
        self.assertEqual('a .PERIOD\nb .PERIOD\n', l)

    def test_ok(self):
        self.assertTrue(add_period.add('a ?QUESTIONMARK olia'))
        self.assertTrue(add_period.add('a !EXCLAMATIONMARK ,COMMA'))

    def test_wrong(self):
        self.assertFalse(add_period.add('a ;SEMICOLON'))
        self.assertFalse(add_period.add('a .PERIOD'))
        self.assertFalse(add_period.add('a ?QUESTIONMARK'))
        self.assertFalse(add_period.add('a !EXCLAMATIONMARK'))


if __name__ == '__main__':
    unittest.main()
