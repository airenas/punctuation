import io
import unittest

import join_colon_sentence


class TestJoinSentence(unittest.TestCase):

    def test_join(self):
        f_in = io.StringIO("a :COLON\nb .PERIOD\n")
        f_out = io.StringIO()
        join_colon_sentence.process(f_in, f_out)
        f_out.seek(0)
        l = f_out.read()
        self.assertEqual('a :COLON b .PERIOD\n', l)

    def test_join_several(self):
        f_in = io.StringIO("a :COLON\nb ;SEMICOLON\nc\nolia\n")
        f_out = io.StringIO()
        join_colon_sentence.process(f_in, f_out)
        f_out.seek(0)
        l = f_out.read()
        self.assertEqual('a :COLON b ;SEMICOLON c\nolia\n', l)

    def test_no_join(self):
        f_in = io.StringIO("a ;SEMICOLON\nc\nolia\n")
        f_out = io.StringIO()
        join_colon_sentence.process(f_in, f_out)
        f_out.seek(0)
        l = f_out.read()
        self.assertEqual('a ;SEMICOLON\nc\nolia\n', l)


if __name__ == '__main__':
    unittest.main()
