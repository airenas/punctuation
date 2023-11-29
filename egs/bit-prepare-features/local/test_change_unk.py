import unittest

import change_unk


class TestChangeUnk(unittest.TestCase):

    def test_no_change(self):
        self.assertEqual(("olia", 0), change_unk.change_word('olia'))
        self.assertEqual(("<NUM>", 0), change_unk.change_word('<NUM>'))
        self.assertEqual(("10-a", 0), change_unk.change_word('10-a'))

    def test_change(self):
        self.assertEqual(('<UNK>', 1), change_unk.change_word('<>'))
        self.assertEqual(('<UNK>', 1), change_unk.change_word('<10,34,3434>'))
        self.assertEqual(('<UNK>', 1), change_unk.change_word('<unk>'))


if __name__ == '__main__':
    unittest.main()
