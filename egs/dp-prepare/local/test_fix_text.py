import unittest

import fix_text


class TestChangeLine(unittest.TestCase):

    def test_brackets(self):
        self.assertEqual(fix_text.change_line('10<>aaa'), '10 aaa')

    def test_url(self):
        self.assertEqual(fix_text.change_line('10<http://olia>aaa'), '10 [URL] aaa')
        self.assertEqual(fix_text.change_line('10<http://olia  aaa >aaa'), '10 [URL] aaa')



if __name__ == '__main__':
    unittest.main()
