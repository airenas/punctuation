import io
import unittest

import drop_period_sentence


class TestJoinSentence(unittest.TestCase):

    def test_leave(self):
        f_in = io.StringIO("a :COLON\nb .PERIOD\n")
        f_out = io.StringIO()
        drop_period_sentence.process(f_in, f_out)
        f_out.seek(0)
        l = f_out.read()
        self.assertEqual('a :COLON\nb .PERIOD\n', l)

    def test_drops(self):
        f_in = io.StringIO("a :COLON\nb .PERIOD ;SEMICOLON\nc\nolia\n")
        f_out = io.StringIO()
        drop_period_sentence.process(f_in, f_out)
        f_out.seek(0)
        l = f_out.read()
        self.assertEqual('a :COLON\nc\nolia\n', l)

    def test_ok(self):
        self.assertTrue(drop_period_sentence.line_ok('a ;SEMICOLON'))
        self.assertTrue(drop_period_sentence.line_ok('a ?QUESTIONMARK'))
        self.assertTrue(drop_period_sentence.line_ok('a !EXCLAMATIONMARK'))

    def test_wrong(self):
        self.assertFalse(drop_period_sentence.line_ok('a .PERIOD a'))
        self.assertFalse(drop_period_sentence.line_ok('a ?QUESTIONMARK b'))
        self.assertFalse(drop_period_sentence.line_ok('a !EXCLAMATIONMARK c'))


if __name__ == '__main__':
    unittest.main()
